#!/usr/bin/env python3
"""Append-only correction of the C27R2 actual-v5 rebuild interface.

The superseded v1 interface used ``atomic_candidate_key`` at the normalized
candidate layer.  That name is ambiguous enough to admit a forbidden adapter
which expands the 101,080 three-terminal candidate pairs into 206,632
``(atom,pair)`` incidences and then counts those incidences as candidates.

Corrected-v2 separates four identities:

* candidate ownership: one row per candidate; T07--T09 have exactly 101,080
  pair candidates and exactly one terminal per pair;
* atom-pair incidence: 206,632 distinct (atom,pair) keys, inheriting the
  already unique terminal of their pair;
* atom disposition: all 483,232 atoms have their exact incidence set or the
  empty complement disposition; and
* physical proof rows: member-pair witnesses from which component edges are
  derived through the frozen C15 map.

The old v1 seal remains byte-preserved but is diagnostic and may not be
consumed by an actual gate.  The actual receipt path/schema is bumped to v2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
OLD_SEAL = (WORKSPACE / ".cm2-runtime/audit/"
            "c27r2-fresh-actual-v5-rebuild-preflight-v1-truthful-reject-seal")
OLD_RECEIPT = OLD_SEAL / "receipt.json"
OLD_ROOT = OLD_SEAL / "root_manifest.sha256"
OLD_TERMINAL = (WORKSPACE / ".cm2-runtime/audit/"
                "c27r2-fresh-actual-v5-rebuild-preflight-v1-truthful-reject-seal-terminal-replay/terminal_replay.json")
NEW_ACTUAL = (WORKSPACE / ".cm2-runtime/audit/"
              "c27-primitive-twenty-family-gate-v5-actual-zero-credit-receipt-v2/receipt.json")

OLD_PINS = {
    OLD_RECEIPT: "e7d1dee54b2edca585f16033ede0ddcc95633de336ef69ad13aea1e5e6d59a39",
    OLD_ROOT: "1c0fe1072cfa5e55f1af7c5ae4abb64cb9c7e330d5885426fa5f98a8d638d80e",
    OLD_TERMINAL: "7c25f1edd9a25785852aa64c07e06bde5130baf2cb94bc6e304e03355bb21196",
}

TERMINALS = (
    "SAME_CHART_RELATIVE_CELLS", "RETAINED_CONTINUATION", "OUTGOING_GRAPHS",
    "SINGLE_GRAPHS", "DOUBLE_GRAPHS", "SHEET_OWNER", "SHEET_SHADOW",
    "SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS", "INCLUDED_STRATUM_ATTACHMENTS",
    "REVERSE_RECHART", "TRUE_CYCLIC_SEAM_E_TO_N",
    "TRUE_CYCLIC_SEAM_N_TO_W", "TRUE_CYCLIC_SEAM_W_TO_S",
    "TRUE_CYCLIC_SEAM_S_TO_E", "Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL", "REPRESENTATION_ALIASES",
)
SLOTS = tuple(f"T{i:02d}_{terminal}" for i, terminal in enumerate(TERMINALS))


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


def corrected_interface() -> dict[str, Any]:
    return {
        "actual_gate_receipt": {
            "path": str(NEW_ACTUAL.relative_to(WORKSPACE)),
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-zero-credit-receipt.v2",
            "closure_field": "receipt_sha256",
        },
        "terminal_order": list(TERMINALS),
        "authority_slot_order": list(SLOTS),
        "candidate_ownership_ledger": {
            "row_schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.candidate-ownership.row.v2",
            "unique_key": "candidate_key",
            "ordering": ["candidate_key"],
            "required_fields": [
                "ordinal", "candidate_key", "candidate_kind", "candidate_pair_key_or_null",
                "terminal_ordinal", "terminal", "authority_slot",
                "primitive_authority_row_sha256", "component_relation_disposition",
                "physical_proof_row_count", "physical_proof_row_sequence_sha256",
                "formal_credit", "row_sha256",
            ],
            "global_rule": "ONE_ROW_PER_CANDIDATE__EXACTLY_ONE_TERMINAL_OWNER",
            "allowed_component_relation_dispositions": [
                "SAME_FROZEN_C15_COMPONENT__NO_EDGE",
                "CROSS_COMPONENT__MATERIALIZED_PHYSICAL_PROOF_REQUIRED",
                "NO_COMPONENT_EDGE_BY_TERMINAL_SEMANTICS",
            ],
            "T00_rule": {
                "candidate_kind": "SAME_CHART_EXACT_CONTACT_CANDIDATE",
                "candidate_count": 5_970_840,
                "strict_volume_candidates": 187_132,
                "lower_dimensional_candidates": 5_783_708,
                "strict_and_lower_disjoint_complete_union": True,
                "C26_691424_is_absence_coverage_theorem_not_candidate_rows": True,
                "G2A_G2B_alias_adds_T00_candidate": False,
                "uses_T07_T09_483232_atom_incidence_layer": False,
            },
            "T07_T08_T09_rule": {
                "candidate_kind": "THREE_TERMINAL_CANDIDATE_PAIR",
                "candidate_count": 101_080,
                "candidate_key_equals_candidate_pair_key": True,
                "terminal_census": {
                    "SIGNED_BOUNDARY_FACES": 25_452,
                    "COMPLETE_BOUNDARY_FACES": 10_688,
                    "POSITIVE_VOLUME_CARRIERS": 64_940,
                },
                "G2A_alias_adds_candidate": False,
            },
        },
        "atom_pair_incidence_ledger": {
            "row_schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.atom-pair-incidence.row.v2",
            "unique_key": ["primitive_support_atom_key", "candidate_pair_key"],
            "ordering": ["primitive_support_atom_key", "candidate_pair_key"],
            "required_fields": [
                "ordinal", "incidence_key", "primitive_support_atom_key",
                "candidate_pair_key", "candidate_terminal", "candidate_owner_row_sha256",
                "formal_credit", "row_sha256",
            ],
            "T07_T08_T09_exact_census": {
                "incidence_count": 206_632,
                "candidate_pair_count": 101_080,
                "primitive_atom_denominator": 483_232,
                "incident_atoms": 62_768,
                "exact_complement_atoms": 420_464,
                "multi_terminal_atoms": 3_896,
            },
            "incidence_creates_new_candidate": False,
            "terminal_must_equal_unique_candidate_pair_owner": True,
            "atom_may_have_multiple_pairs_and_terminals": True,
        },
        "atom_incidence_disposition_ledger": {
            "row_schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.atom-incidence-disposition.row.v2",
            "unique_key": "primitive_support_atom_key",
            "row_count": 483_232,
            "required_fields": [
                "ordinal", "primitive_support_atom_key", "incidence_count",
                "incidence_row_sequence_sha256", "terminal_set",
                "disposition", "formal_credit", "row_sha256",
            ],
            "allowed_dispositions": [
                "EXACT_NONEMPTY_ATOM_PAIR_INCIDENCE_SET",
                "EXACT_EMPTY_INCIDENCE_COMPLEMENT",
            ],
        },
        "materialized_physical_proof_join_ledger": {
            "row_schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.materialized-physical-proof-join.row.v2",
            "unique_key": "proof_row_key",
            "required_fields": [
                "ordinal", "proof_row_key", "candidate_key",
                "atom_pair_incidence_key_or_null", "terminal", "authority_slot",
                "primitive_authority_row_sha256", "ordered_C15_member_pair",
                "ordered_C15_component_pair", "component_edge_key",
                "physical_witness_key", "formal_credit", "row_sha256",
            ],
            "incidence_row_is_not_automatically_a_physical_proof": True,
            "member_pair_maps_through_frozen_C15": True,
        },
        "full_component_edge_union_ledger": {
            "row_schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual.full-component-edge-union.row.v2",
            "unique_key": "component_edge_key",
            "candidate_universe": False,
            "exact_source": "DISTINCT_CROSS_COMPONENT_PAIRS_DERIVED_FROM_MATERIALIZED_PHYSICAL_PROOF_MEMBER_PAIRS",
        },
        "prohibited_conflations": [
            "ATOM_PAIR_INCIDENCE_AS_CANDIDATE",
            "206632_INCIDENCES_AS_206632_NORMALIZED_CANDIDATES",
            "PRIMITIVE_ATOM_AS_CANDIDATE_PAIR",
            "PHYSICAL_PROOF_ROW_AS_CANDIDATE_OWNERSHIP_ROW",
            "CURRENT_ONLY_197224_INCIDENCES_AS_FULL_INCIDENCE_AUTHORITY",
        ],
        "fixed_frozen_C15_census": {"members": 502_204, "components": 57_876},
        "global_other_terminal_candidate_counts": "DERIVE_FROM_FRESH_PRIMITIVE_AUTHORITIES__DO_NOT_HARDCODE_OR_INFER_FROM_RECEIPT_CENSUS_ONLY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--notice", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        for path, pin in OLD_PINS.items():
            need(path.is_file() and fsha(path) == pin, "old artifact pin:" + path.name)
        old_receipt = json.loads(OLD_RECEIPT.read_bytes())
        need(old_receipt.get("receipt_sha256") ==
             "f9c8f7e6d74cedd3c722eab9c580db3a5834cf879d785b383cde01846815ecac",
             "old receipt object pin")
        notice_body = {
            "schema": "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-interface-v1-invalidation.v2",
            "status": "INVALIDATED_FOR_ACTUAL_GATE_CONSUMPTION__DIAGNOSTIC_ONLY__CORRECTED_V2_REQUIRED",
            "invalidated_receipt_path": str(OLD_RECEIPT.relative_to(WORKSPACE)),
            "invalidated_receipt_file_sha256": OLD_PINS[OLD_RECEIPT],
            "invalidated_receipt_object_sha256": old_receipt["receipt_sha256"],
            "old_files_modified": False,
            "reason": "ATOMIC_CANDIDATE_KEY_AMBIGUOUSLY_ADMITTED_ATOM_PAIR_INCIDENCE_AS_NORMALIZED_CANDIDATE",
            "forbidden_observed_adapter_semantics": "206632_ATOM_PAIR_INCIDENCES_COUNTED_AS_NORMALIZED_CANDIDATES",
            "correct_semantics": "101080_CANDIDATE_PAIRS_EACH_ONE_TERMINAL__206632_INCIDENCES_SEPARATE",
            "old_v1_actual_receipt_path_may_authorize": False,
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27_C28_C29": "UNAUTHORIZED",
            "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        notice_body["notice_sha256"] = digest(notice_body)
        write_new(Path(args.notice), notice_body)
        notice_file_sha = fsha(Path(args.notice))

        interface = corrected_interface()
        missing = [] if NEW_ACTUAL.exists() else ["ACTUAL_V5_TWENTY_FAMILY_TERMINAL_RECEIPT_V2"]
        body = {
            "schema": "cm2.round306c27r2.source-g-fresh-actual-v5-rebuild-interface-correction-preflight.v2",
            "status": "REJECT_CORRECTED_V2_ACTUAL_GATE_RECEIPT_MISSING__ZERO_CREDIT",
            "decision": "REJECT",
            "intended_process_exit_code": 2,
            "append_only_supersession": {
                "v1_receipt_disposition": "DIAGNOSTIC_ONLY__MAY_NOT_BE_CONSUMED",
                "v1_files_modified": False,
                "invalidation_notice_path": str(Path(args.notice).resolve().relative_to(WORKSPACE)),
                "invalidation_notice_file_sha256": notice_file_sha,
                "invalidation_notice_object_sha256": notice_body["notice_sha256"],
            },
            "semantic_judgment": {
                "corrected_v2_candidate_identity": "CANDIDATE_PAIR_AT_T07_T09__NOT_ATOM_PAIR_INCIDENCE",
                "T07_T09_candidate_pair_count": 101_080,
                "T07_T09_atom_pair_incidence_count": 206_632,
                "incidence_may_count_as_candidate": False,
                "candidate_pair_each_exactly_one_terminal": True,
                "atom_pair_incidence_inherits_pair_terminal": True,
            },
            "corrected_interface": interface,
            "missing_required_authority": missing,
            "actual_gate_v1_receipt_accepted": False,
            "actual_gate_v2_receipt_present": NEW_ACTUAL.exists(),
            "fresh_C27R2_producer_may_start": False,
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27_transition_totality": "UNAUTHORIZED",
            "C28_pair_routing": "UNAUTHORIZED",
            "C29_physical_maximality": "UNAUTHORIZED",
            "Source_W_transition_authorized": False,
            "Source_W_formal_remainder": 80,
            "CM2": "NO-GO_FOR_CLAIM",
        }
        body["preflight_sha256"] = digest(body)
        write_new(Path(args.output), body)
    except (Failure, KeyError, TypeError, ValueError, OSError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": body["status"],
                     "preflight_sha256": body["preflight_sha256"],
                     "notice_sha256": notice_body["notice_sha256"]}).decode("ascii"))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
