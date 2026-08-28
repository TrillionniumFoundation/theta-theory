#!/usr/bin/env python3
"""No-import verifier for the post-actual-v5 C27R2/C28/C29 preflight."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
from typing import Any


WORKSPACE = Path(__file__).resolve().parent.parent
ACTUAL = (WORKSPACE / ".cm2-runtime/audit/"
          "c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v2/receipt.json")

DISPOSITIONS = {
    "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 65_064,
    "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 264_156,
    "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 7_156_856,
}

EXPECTED_SEALS = {
    "T04_DOUBLE_GRAPHS": (
        "007b9162a83d9cb665c72ec123253f6eab6d6b831e3225a0bafb585f256150d7",
        "a2601fa76add2d86ca87b12cdb16109d799bcc760ac491223e8a34036d44d87e"),
    "T01_T02_T03_T05_T06_T10": (
        "4fd0ae953336743384967c1f3a05712df5cdcae4076240b75f73863829ea9598",
        "2f56d9cba3f0cb0e23a42c10c34795d63291087f5589de32e579ec925543c9b0"),
    "T07_T08_T09": (
        "6a9c5c28863948f2fb5c122b7d7139db6e774d328064e0c91d3c7a7172d17a1b",
        "fbf7c43e933443b8fe11d06d0b927601d80cd3a0a056aab39f263d774134aa87"),
    "T11_T19": (
        "3a697d2e1e18aee57c3fed205193cf2b84fb9f305817544bf070e9741a8ac293",
        "5738daf2e15dace9a4e16204d93b1d4c5239918d52310b58fceeb01debb883b5"),
}

ALLOWED_IMPORT_ROOTS = {
    "__future__", "argparse", "ast", "collections", "gzip", "hashlib",
    "json", "os", "pathlib", "sqlite3", "stat", "tempfile", "typing",
}


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
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_new(path: Path, value: dict[str, Any]) -> None:
    path = path.resolve()
    need(path.is_relative_to(WORKSPACE), "output:workspace")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def validate_source(path: Path, expected: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == expected, "producer:sha")
    tree = ast.parse(raw, filename=str(path))
    imported = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.append((node.module or "").split(".", 1)[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            need(node.func.id not in {"eval", "exec", "__import__"},
                 "producer:dynamic-import-or-exec")
    need(set(imported) <= ALLOWED_IMPORT_ROOTS, "producer:workspace-import")
    text = raw.decode("utf-8")
    for forbidden in (
        "cm2_round306c27_transition_family_coverage_ledger",
        "cm2_round306c28_", "cm2_round306c29_",
        "round306c27_source_g_transition_candidate_ledger",
    ):
        need(forbidden not in text, "producer:forbidden-path-token:" + forbidden)
    return {"source_sha256": expected, "producer_module_imported": False,
            "stdlib_import_roots": sorted(set(imported))}


def validate_receipt(receipt_path: Path, producer_path: Path) -> dict[str, Any]:
    raw = receipt_path.read_bytes()
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw, "receipt:canonical")
    body = dict(value)
    closure = body.pop("preflight_sha256", None)
    need(type(closure) is str and closure == digest(body), "receipt:closure")
    need(value.get("schema") == "cm2.round306c27r2-c28-c29.post-actual-v5-rebuild-preflight.v2",
         "receipt:schema")
    need(value.get("status") ==
         "REJECT_ACTUAL_V5_TERMINAL_RECEIPT_V2_MISSING__PIPELINE_ARMED_FAIL_CLOSED_ZERO_CREDIT",
         "receipt:status")
    need(value.get("decision") == "REJECT" and value.get("intended_process_exit_code") == 2,
         "receipt:truthful-reject")
    need(value.get("observed_actual_gate_receipt_present") is False and not ACTUAL.exists(),
         "receipt:actual-absent")
    need(value.get("blocking_authorities") == [
        "ACTUAL_V5_TWENTY_FAMILY_TERMINAL_RECEIPT_V2",
        "T00_SEALED_SUBAUTHORITY_TRANSITIVELY_REQUIRED_BY_ACTUAL_V5"],
         "receipt:blockers")
    need(value.get("sealed_subauthority_subtotal") == {
        "candidate_count": 1_515_236, "proof_count": 32_824,
        "dispositions": {
            "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 32_824,
            "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 109_264,
            "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 1_373_148,
        }}, "receipt:sealed-subtotal")
    need(value.get("T00_expected_reconciliation_not_yet_consumed") == {
        "candidate_count": 5_970_840, "proof_count": 32_240,
        "dispositions": {
            "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED": 32_240,
            "SAME_FROZEN_C15_COMPONENT__NO_EDGE": 154_892,
            "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS": 5_783_708,
        },
        "future_seal_receipt_path": ".cm2-runtime/audit/c27-primitive-v5-actual-t00-same-chart-exact-contact-adapter-v2-zero-credit-seal-v1/receipt.json",
    }, "receipt:T00-reconciliation")
    need(value.get("eventual_exact_global_conservation") == {
        "candidate_count": 7_486_076, "proof_count": 65_064,
        "dispositions": DISPOSITIONS, "disposition_sum": 7_486_076,
    }, "receipt:global-conservation")
    need(value.get("corrected_interface_object_sha256") ==
         "3ece982b83b968e7cc23c4d43f2602fb5f8490484af5ed2f214515be4f0eb37e",
         "receipt:corrected-interface")

    consumed = value.get("sealed_subauthorities_consumed")
    need(type(consumed) is list and len(consumed) == 4, "receipt:sealed-input-count")
    labels = set()
    for item in consumed:
        label = item.get("label")
        need(label in EXPECTED_SEALS and label not in labels, "receipt:sealed-label")
        labels.add(label)
        receipt_att, replay_att = item.get("receipt"), item.get("cold_replay")
        need(type(receipt_att) is dict and type(replay_att) is dict,
             "receipt:sealed-attestation")
        expected_receipt, expected_replay = EXPECTED_SEALS[label]
        need(receipt_att.get("sha256") == expected_receipt
             and replay_att.get("sha256") == expected_replay,
             "receipt:sealed-pin:" + label)
        for att in (receipt_att, replay_att):
            path = (WORKSPACE / att["path"]).resolve()
            need(path.is_relative_to(WORKSPACE) and path.is_file(), "receipt:sealed-path")
            need(fsha(path) == att["sha256"] and path.stat().st_size == att["size"],
                 "receipt:sealed-file")
            need(att.get("O_NOFOLLOW") is True
                 and att.get("single_open_file_description_hash_parse_fstat") is True,
                 "receipt:sealed-capture")
    need(labels == set(EXPECTED_SEALS), "receipt:sealed-complete")

    contract = value.get("pipeline_contract")
    need(type(contract) is dict, "contract:object")
    need(contract["actual_gate_receipt"] == {
        "path": ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v2/receipt.json",
        "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-zero-credit-receipt.v2",
        "closure_field": "receipt_sha256",
        "required_top_level_descriptors": ["terminal_authority_descriptors", "materialized_ledger_descriptors"],
    }, "contract:actual")
    need(contract["global_candidate_ownership"]["exact_rows"] == 7_486_076
         and contract["global_candidate_ownership"]["one_row_one_terminal"] is True
         and contract["global_candidate_ownership"]["streaming_validation"] is True,
         "contract:candidates")
    need(contract["candidate_component_disposition_conservation"] == DISPOSITIONS,
         "contract:dispositions")
    proof = contract["materialized_physical_proof_join"]
    need(proof["exact_rows"] == 65_064
         and proof["ordering"] == ["candidate_key", "proof_row_key"]
         and proof["exactly_one_proof_for_each_cross_candidate"] is True
         and proof["zero_proofs_for_non_cross_candidates"] is True
         and proof["member_pair_rederived_through_frozen_C15"] is True,
         "contract:proof")
    edge = contract["full_component_edge_union"]
    need(edge["ordering"] == ["component_edge_key"]
         and edge["diagnostic_expected_count_not_authority"] == 14_860
         and edge["historical_14772_or_14724_accepted_as_authority"] is False,
         "contract:edge")
    need(contract["fresh_C29"]["frozen_C15"] == {
        "members": 502_204, "components": 57_876,
        "path": "deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz",
        "size": 142_025_813,
        "sha256": "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a",
    }, "contract:C15")
    need(contract["fresh_C29"]["diagnostic_expected_final_components_not_authority"] == 43_684,
         "contract:DSU-diagnostic")
    need(set(contract["forbidden_dependencies"].values()) == {False},
         "contract:forbidden-governance")

    need(value.get("fresh_C27R2_C28_C29_producer_may_start") is False
         and value.get("formal_credit") == 0 and value.get("manifest_authorized") is False
         and value.get("C27R2") == value.get("C28") == value.get("C29") == "UNAUTHORIZED"
         and value.get("Source_W_transition_authorized") is False
         and value.get("Source_W_formal_remainder") == 80
         and value.get("CM2") == "NO-GO_FOR_CLAIM", "receipt:nonpromotion")
    source = validate_source(producer_path, value.get("producer_source_sha256"))
    return {
        "receipt_file_sha256": fsha(receipt_path),
        "receipt_object_sha256": closure,
        "source_validation": source,
        "sealed_subauthority_count": 4,
        "eventual_candidate_rows": 7_486_076,
        "eventual_proof_rows": 65_064,
        "actual_gate_missing": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--producer", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        details = validate_receipt(Path(args.receipt).resolve(), Path(args.producer).resolve())
        body = {
            "schema": "cm2.round306c27r2-c28-c29.post-actual-v5-rebuild-preflight-independent-verification.v2",
            "status": "PASS_NO_IMPORT_TRUTHFUL_REJECT_AND_EVENTUAL_STREAMING_CONTRACT_VERIFIED__ZERO_CREDIT",
            "decision": "PASS", "details": details,
            "coherent_mutation_input_accepted": False,
            "formal_credit": 0, "manifest_authorized": False,
            "C27R2_C28_C29": "UNAUTHORIZED", "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        body["verification_sha256"] = digest(body)
        append_new(Path(args.output), body)
        return 0
    except (Failure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError,
            SyntaxError) as exc:
        print("REJECT:" + str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
