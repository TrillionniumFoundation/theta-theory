#!/usr/bin/env python3
"""Independent verifier for the legacy-16 authority normalization reject."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent

TERMINALS = (
    "RETAINED_CONTINUATION", "OUTGOING_GRAPHS", "SINGLE_GRAPHS",
    "DOUBLE_GRAPHS", "SHEET_OWNER", "SHEET_SHADOW",
    "INCLUDED_STRATUM_ATTACHMENTS", "REVERSE_RECHART",
    "TRUE_CYCLIC_SEAM_E_TO_N", "TRUE_CYCLIC_SEAM_N_TO_W",
    "TRUE_CYCLIC_SEAM_W_TO_S", "TRUE_CYCLIC_SEAM_S_TO_E",
    "Jx_NEGATIVE_CONTROL", "Jy_NEGATIVE_CONTROL",
    "JxJy_NEGATIVE_CONTROL", "REPRESENTATION_ALIASES",
)
GAPS = frozenset({
    "DOUBLE_GRAPHS", "REVERSE_RECHART", "TRUE_CYCLIC_SEAM_E_TO_N",
    "TRUE_CYCLIC_SEAM_N_TO_W", "TRUE_CYCLIC_SEAM_W_TO_S",
    "TRUE_CYCLIC_SEAM_S_TO_E", "Jx_NEGATIVE_CONTROL",
    "Jy_NEGATIVE_CONTROL", "JxJy_NEGATIVE_CONTROL",
    "REPRESENTATION_ALIASES",
})
RECEIPT_BACKED = frozenset(set(TERMINALS) - GAPS)


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


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def closed(value: dict[str, Any], key: str, label: str) -> None:
    claim = value.get(key)
    body = dict(value)
    body.pop(key, None)
    need(type(claim) is str and claim == digest(body), label + ":closure")


def gz_rows(path: Path) -> list[dict[str, Any]]:
    output = []
    with gzip.open(path, "rt", encoding="ascii") as handle:
        for ordinal, line in enumerate(handle):
            value = json.loads(line)
            need(type(value) is dict, f"row:{ordinal}:object")
            closed(value, "row_sha256", f"row:{ordinal}")
            output.append(value)
    return output


def verify(args: argparse.Namespace) -> dict[str, Any]:
    result_path = Path(args.result)
    normalized_path = Path(args.normalized)
    gap_path = Path(args.gaps)
    result = json.loads(result_path.read_bytes())
    need(type(result) is dict, "result object")
    closed(result, "result_sha256", "result")
    rows = gz_rows(normalized_path)
    gaps = gz_rows(gap_path)

    need(result["schema"] ==
         "cm2.c27-independent.legacy16-terminal-authority-normalization.result.v1"
         and result["status"] ==
         "REJECT_ACTUAL_V5_LEGACY16_AUTHORITY_INCOMPLETE__6_RECEIPT_BACKED__10_HARD_GAPS__ZERO_CREDIT"
         and result["decision"] == "FAIL_CLOSED_REJECT"
         and result["formal_credit"] == 0
         and result["manifest_authorized"] is False
         and result["source_W_transition_authorized"] is False,
         "truthful reject result")
    need(result["terminal_census"] == {
        "requested": 16, "receipt_backed_terminal_authorities": 6,
        "receipt_and_materialized_row_authorities": 5,
        "receipt_commitment_only_no_candidate_ledger": 1,
        "hard_terminal_authority_gaps": 10}, "terminal census")
    need(tuple(item["terminal"] for item in rows) == TERMINALS
         and [item["ordinal"] for item in rows] == list(range(16)),
         "terminal sequence")
    need({item["terminal"] for item in rows
          if not item["terminal_formal_authority_blocking_gap"]}
         == RECEIPT_BACKED, "receipt-backed partition")
    need({item["terminal"] for item in rows
          if item["terminal_formal_authority_blocking_gap"]} == GAPS,
         "hard-gap partition")
    need(all(item["formal_credit"] == 0
             and item["source_W_transition_authorized"] is False
             and len(item["normalized_candidate_key_fields"]) > 0
             for item in rows), "normalized row governance")

    expected_counts = {
        "RETAINED_CONTINUATION": 276, "OUTGOING_GRAPHS": 264,
        "SINGLE_GRAPHS": 4_984, "DOUBLE_GRAPHS": 16,
        "SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940,
        "INCLUDED_STRATUM_ATTACHMENTS": 10_660, "REVERSE_RECHART": 4,
        "TRUE_CYCLIC_SEAM_E_TO_N": 1, "TRUE_CYCLIC_SEAM_N_TO_W": 1,
        "TRUE_CYCLIC_SEAM_W_TO_S": 1, "TRUE_CYCLIC_SEAM_S_TO_E": 1,
        "Jx_NEGATIVE_CONTROL": 1, "Jy_NEGATIVE_CONTROL": 1,
        "JxJy_NEGATIVE_CONTROL": 1, "REPRESENTATION_ALIASES": 276,
    }
    need({item["terminal"]: item["candidate_count"] for item in rows}
         == expected_counts, "candidate counts")

    by_name = {item["terminal"]: item for item in rows}
    need(by_name["DOUBLE_GRAPHS"]["authority_class"]
         == "REJECTED_DIAGNOSTIC_ONLY"
         and by_name["DOUBLE_GRAPHS"]["absence_disposition_contract"]
             ["unresolved_candidate_count"] == 1_361_872,
         "double remains reject")
    need(by_name["INCLUDED_STRATUM_ATTACHMENTS"]["authority_class"]
         == "RECEIPT_COMMITMENT_ONLY_NO_MATERIALIZED_CANDIDATE_LEDGER"
         and by_name["INCLUDED_STRATUM_ATTACHMENTS"]["candidate_ledger"] is None,
         "included commitment only")
    need(by_name["REPRESENTATION_ALIASES"]["candidate_ledger"]
             ["same_rows_already_bound_to_retained_continuation"] is True,
         "alias/retained evidence reuse")

    need(len(gaps) == 10 and {item["terminal"] for item in gaps} == GAPS
         and [item["gap_ordinal"] for item in gaps] == list(range(10))
         and all(item["gate_blocking"] is True
                 and item["formal_credit"] == 0
                 and len(item["missing"]) > 0 for item in gaps),
         "gap ledger exactness")

    need(file_hash(normalized_path) == result["normalized_ledger"]["file_sha256"]
         and len(rows) == result["normalized_ledger"]["row_count"]
         and digest([item["row_sha256"] for item in rows])
             == result["normalized_ledger"]["row_sequence_sha256"],
         "normalized ledger binding")
    need(file_hash(gap_path) == result["gap_ledger"]["file_sha256"]
         and len(gaps) == result["gap_ledger"]["row_count"]
         and digest([item["row_sha256"] for item in gaps])
             == result["gap_ledger"]["row_sequence_sha256"],
         "gap ledger binding")

    # Rehash every authority input independently.  No producer module is
    # imported and no conclusion is trusted merely because it was serialized.
    for label, record in result["input_pins"].items():
        path = ROOT / record["path"]
        need(path.is_file() and not path.is_symlink(), label + ":regular")
        need(file_hash(path) == record["sha256"], label + ":sha256")

    contract = result["actual_v5_contract"]
    need(contract == {
        "must_bind_all_six_receipt_backed_authorities": True,
        "must_close_all_ten_hard_gaps_with_terminal_level_authority": True,
        "may_not_treat_old_16_of_20_aggregate_census_as_authority": True,
        "may_not_set_primitive_twenty_family_totality_proved_now": True,
        "strict14772_or_scoped14724_used_as_candidate_universe": False},
         "actual-v5 fail-closed contract")
    governance = result["forbidden_input_governance"]
    need(all(value is False for value in governance.values()),
         "forbidden input governance")
    need(result["strict_nonpromotion"] == {
        "C27_transition_totality": 0, "C28_pair_routing": 0,
        "C29_physical_maximality": 0, "CM2": "NO-GO_FOR_CLAIM"},
         "strict nonpromotion")

    body = {
        "schema": "cm2.c27-independent.legacy16-terminal-authority-normalization.verification.v1",
        "status": "PASS_INDEPENDENT_LEGACY16_NORMALIZATION__TRUTHFUL_REJECT_6_RECEIPT_BACKED_10_HARD_GAPS__ZERO_CREDIT",
        "producer_imported_or_executed": False,
        "normalized_rows": 16, "receipt_backed": 6, "hard_gaps": 10,
        "all_input_pins_rehashed": True,
        "result_file_sha256": file_hash(result_path),
        "normalized_file_sha256": file_hash(normalized_path),
        "gap_file_sha256": file_hash(gap_path),
        "formal_credit": 0, "manifest_authorized": False,
        "source_W_transition_authorized": False,
    }
    return {**body, "verification_sha256": digest(body)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True)
    parser.add_argument("--normalized", required=True)
    parser.add_argument("--gaps", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        value = verify(args)
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    if args.output:
        output = Path(args.output)
        need(not output.exists(), "fresh verification output")
        output.write_bytes(canonical(value) + b"\n")
    print(canonical(value).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
