#!/usr/bin/env python3
"""Independent no-producer-import verifier for C27R2 interface correction-v2."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
OLD_RECEIPT = (WORKSPACE / ".cm2-runtime/audit/"
               "c27r2-fresh-actual-v5-rebuild-preflight-v1-truthful-reject-seal/receipt.json")
NEW_ACTUAL = (WORKSPACE / ".cm2-runtime/audit/"
              "c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v2/receipt.json")
TERMINALS = [
    "SAME_CHART_RELATIVE_CELLS", "RETAINED_CONTINUATION", "OUTGOING_GRAPHS",
    "SINGLE_GRAPHS", "DOUBLE_GRAPHS", "SHEET_OWNER", "SHEET_SHADOW",
    "SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS", "INCLUDED_STRATUM_ATTACHMENTS",
    "REVERSE_RECHART", "TRUE_CYCLIC_SEAM_E_TO_N",
    "TRUE_CYCLIC_SEAM_N_TO_W", "TRUE_CYCLIC_SEAM_W_TO_S",
    "TRUE_CYCLIC_SEAM_S_TO_E", "Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL", "REPRESENTATION_ALIASES",
]
SLOTS = [f"T{i:02d}_{terminal}" for i, terminal in enumerate(TERMINALS)]


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def fsha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def closed(path: Path, field: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and b"\n" not in raw[:-1], "single:" + str(path))
    value = json.loads(raw[:-1])
    need(type(value) is dict and canonical(value) == raw[:-1], "canonical:" + str(path))
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body), "closure:" + str(path))
    return value


def verify_document(value: dict[str, Any], notice: dict[str, Any]) -> dict[str, Any]:
    body = dict(value)
    claimed = body.pop("preflight_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "preflight closure")
    need(value.get("schema") ==
         "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-interface-correction-preflight.v2",
         "schema")
    need(value.get("status") ==
         "REJECT_CORRECTED_V2_ACTUAL_GATE_RECEIPT_MISSING__ZERO_CREDIT"
         and value.get("decision") == "REJECT"
         and value.get("intended_process_exit_code") == 2,
         "truthful reject")
    sup = value.get("append_only_supersession", {})
    need(sup.get("v1_receipt_disposition") ==
         "DIAGNOSTIC_ONLY__MAY_NOT_BE_CONSUMED"
         and sup.get("v1_files_modified") is False
         and sup.get("invalidation_notice_object_sha256") == notice["notice_sha256"],
         "v1 supersession")
    need(not value.get("actual_gate_v1_receipt_accepted")
         and not value.get("actual_gate_v2_receipt_present")
         and value.get("missing_required_authority") ==
         ["ACTUAL_V5_TWENTY_FAMILY_TERMINAL_RECEIPT_V2"],
         "actual-v2 missing")
    judgment = value.get("semantic_judgment", {})
    need(judgment == {
        "corrected_v2_candidate_identity":
            "CANDIDATE_PAIR_AT_T07_T09__NOT_ATOM_PAIR_INCIDENCE",
        "T07_T09_candidate_pair_count": 101_080,
        "T07_T09_atom_pair_incidence_count": 206_632,
        "incidence_may_count_as_candidate": False,
        "candidate_pair_each_exactly_one_terminal": True,
        "atom_pair_incidence_inherits_pair_terminal": True,
    }, "semantic judgment")
    interface = value.get("corrected_interface", {})
    receipt = interface.get("actual_gate_receipt", {})
    need(receipt.get("path") ==
         ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v2/receipt.json"
         and receipt.get("schema") ==
         "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-zero-credit-receipt.v2",
         "actual v2 receipt")
    need(interface.get("terminal_order") == TERMINALS
         and interface.get("authority_slot_order") == SLOTS,
         "terminal/slot order")
    candidate = interface.get("candidate_ownership_ledger", {})
    need(candidate.get("row_schema") ==
         "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2"
         and candidate.get("unique_key") == "candidate_key",
         "candidate schema")
    t00 = candidate.get("T00_rule", {})
    need(t00.get("candidate_count") == 5_970_840
         and t00.get("strict_volume_candidates") == 187_132
         and t00.get("lower_dimensional_candidates") == 5_783_708
         and t00.get("C26_691424_is_absence_coverage_theorem_not_candidate_rows") is True
         and t00.get("G2A_G2B_alias_adds_T00_candidate") is False
         and t00.get("uses_T07_T09_483232_atom_incidence_layer") is False,
         "T00 semantics")
    t079 = candidate.get("T07_T08_T09_rule", {})
    need(t079.get("candidate_count") == 101_080
         and t079.get("candidate_key_equals_candidate_pair_key") is True
         and t079.get("terminal_census") == {
             "SIGNED_BOUNDARY_FACES": 25_452,
             "COMPLETE_BOUNDARY_FACES": 10_688,
             "POSITIVE_VOLUME_CARRIERS": 64_940,
         } and t079.get("G2A_alias_adds_candidate") is False,
         "T07-T09 candidate layer")
    incidence = interface.get("atom_pair_incidence_ledger", {})
    need(incidence.get("row_schema") ==
         "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.atom-pair-incidence.row.v2"
         and incidence.get("unique_key") ==
         ["primitive_support_atom_key", "candidate_pair_key"]
         and incidence.get("T07_T08_T09_exact_census") == {
             "incidence_count": 206_632, "candidate_pair_count": 101_080,
             "primitive_atom_denominator": 483_232, "incident_atoms": 62_768,
             "exact_complement_atoms": 420_464, "multi_terminal_atoms": 3_896,
         } and incidence.get("incidence_creates_new_candidate") is False
         and incidence.get("atom_may_have_multiple_pairs_and_terminals") is True,
         "incidence layer")
    atom = interface.get("atom_incidence_disposition_ledger", {})
    need(atom.get("row_count") == 483_232
         and atom.get("unique_key") == "primitive_support_atom_key",
         "atom disposition")
    proof = interface.get("materialized_physical_proof_join_ledger", {})
    need(proof.get("incidence_row_is_not_automatically_a_physical_proof") is True
         and "ordered_C15_member_pair" in proof.get("required_fields", [])
         and "physical_witness_key" in proof.get("required_fields", []),
         "physical proof separation")
    edge = interface.get("full_component_edge_union_ledger", {})
    need(edge.get("candidate_universe") is False
         and edge.get("exact_source") ==
         "DISTINCT_CROSS_COMPONENT_PAIRS_DERIVED_FROM_MATERIALIZED_PHYSICAL_PROOF_MEMBER_PAIRS",
         "edge derivation")
    prohibited = interface.get("prohibited_conflations", [])
    need("206632_INCIDENCES_AS_206632_NORMALIZED_CANDIDATES" in prohibited
         and "ATOM_PAIR_INCIDENCE_AS_CANDIDATE" in prohibited,
         "prohibited conflations")
    need(value.get("fresh_C27R2_producer_may_start") is False
         and value.get("formal_credit") == 0
         and value.get("manifest_authorized") is False
         and value.get("C27_transition_totality") == "UNAUTHORIZED"
         and value.get("C28_pair_routing") == "UNAUTHORIZED"
         and value.get("C29_physical_maximality") == "UNAUTHORIZED"
         and value.get("Source_W_formal_remainder") == 80
         and value.get("CM2") == "NO-GO_FOR_CLAIM",
         "nonpromotion")
    return {"preflight_sha256": claimed, "semantic_correction_verified": True}


def write_new(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = canonical(value) + b"\n"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                 | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", required=True)
    parser.add_argument("--notice", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        need(fsha(OLD_RECEIPT) ==
             "e7d1dee54b2edca585f16033ede0ddcc95633de336ef69ad13aea1e5e6d59a39",
             "old receipt preserved")
        need(not NEW_ACTUAL.exists(), "new actual receipt must be absent")
        notice = closed(Path(args.notice), "notice_sha256")
        need(notice.get("status") ==
             "INVALIDATED_FOR_ACTUAL_GATE_CONSUMPTION__DIAGNOSTIC_ONLY__CORRECTED_V2_REQUIRED"
             and notice.get("old_files_modified") is False
             and notice.get("old_v1_actual_receipt_path_may_authorize") is False,
             "notice semantics")
        preflight = closed(Path(args.preflight), "preflight_sha256")
        verified = verify_document(preflight, notice)
        result = {
            "schema": "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-interface-correction-v2.independent-verification.v1",
            "status": "PASS_INDEPENDENT_CANDIDATE_VS_INCIDENCE_SEPARATION_AND_V1_INVALIDATION__ZERO_CREDIT",
            "verified": verified,
            "producer_module_imported": False,
            "old_v1_files_preserved": True,
            "formal_credit": 0,
            "manifest_authorized": False,
        }
        result["verification_sha256"] = digest(result)
        write_new(Path(args.output), result)
    except (Reject, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "verification_sha256": result["verification_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
