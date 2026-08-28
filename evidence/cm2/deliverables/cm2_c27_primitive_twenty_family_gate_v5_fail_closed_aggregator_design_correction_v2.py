#!/usr/bin/env python3
"""Append-only correction to the v5 fail-closed aggregator design.

The v1 design incorrectly imposed at-most-one pair/terminal on each support
atom.  This correction quarantines those clauses.  Uniqueness is per candidate
pair; an atom owns an exact, duplicate-free set of zero or more pair
incidences and may consequently meet multiple terminals.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def build() -> dict[str, Any]:
    body = {
        "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-aggregator-design-correction.v2",
        "status": "CORRECTED_DESIGN_READY__V1_IMPOSSIBLE_ATOM_UNIQUENESS_QUARANTINED__TRUTHFUL_REJECT__ZERO_CREDIT",
        "append_only_supersession": {
            "superseded_design_path": (
                ".cm2-runtime/audit/c27-primitive-twenty-family-gate-v5-"
                "fail-closed-design/design.json"
            ),
            "superseded_design_file_sha256": (
                "cd427c89d56181e078e662f26c7b6797f03706f735a09479d2d5b868f8e08a9a"
            ),
            "superseded_design_object_sha256": (
                "30b66e9c108658707de01478ad1479bbd3c6631089d5a9f1b0b0886b59b652c5"
            ),
            "old_file_modified": False,
            "v1_may_not_authorize_any_gate": True,
            "v1_disposition": "QUARANTINED_DIAGNOSTIC_DESIGN_ERROR",
        },
        "quarantined_v1_clauses": [
            "EVERY_DENOMINATOR_ATOM_HAS_ZERO_OR_ONE_PAIR_INCIDENCE",
            "EVERY_INCIDENT_ATOM_HAS_EXACTLY_ONE_TERMINAL",
            "REQUIRE_ONE_TERMINAL_PER_INCIDENT_ATOM_AND_NO_G2A_G2B_DOUBLE_COUNT",
            "ATOM_LAYER_EXHAUSTIVE_AND_MUTUALLY_EXCLUSIVE_TERMINAL_SELECTION",
        ],
        "evidence_demonstrating_v1_is_impossible": {
            "current_only_incident_atom_count": 62_240,
            "current_only_expanded_incidence_count": 197_408,
            "current_only_multi_terminal_atom_count": 3_896,
            "multi_pair_atom_is_legal": True,
            "multi_terminal_atom_is_legal": True,
            "these_censuses_are_contract_inputs_not_recomputed_by_design_emitter": True,
        },
        "corrected_uniqueness_levels": {
            "candidate_pair": {
                "each_pair_has_exactly_one_assigned_terminal": True,
                "allowed_terminals": [
                    "SIGNED_BOUNDARY_FACES",
                    "COMPLETE_BOUNDARY_FACES",
                    "POSITIVE_VOLUME_CARRIERS",
                ],
                "same_pair_may_not_be_emitted_twice": True,
                "G2A_alias_may_not_create_second_pair_or_terminal_assignment": True,
            },
            "atom_pair_incidence": {
                "incidence_key": ["primitive_support_atom_key", "candidate_pair_key"],
                "duplicate_incidence_key_forbidden": True,
                "every_incident_pair_must_exist_in_full_101080_pair_authority": True,
                "every_incidence_inherits_the_unique_terminal_of_its_pair": True,
                "one_atom_may_have_multiple_distinct_pair_incidences": True,
                "one_atom_may_therefore_observe_multiple_distinct_terminals": True,
            },
            "atom": {
                "each_atom_has_an_exact_materialized_incidence_set": True,
                "empty_incidence_set_is_the_atom_complement_disposition": True,
                "nonempty_incidence_set_cardinality_may_exceed_one": True,
                "atom_terminal_uniqueness_required": False,
                "atom_terminal_mutual_exclusivity_required": False,
            },
        },
        "corrected_full_union_atom_contract": {
            "primitive_support_atom_denominator": 483_232,
            "full_pair_authority_row_count": 101_080,
            "requirements": [
                "CURRENT_91672_PAIR_ROUTES_BOUND",
                "C24A_G2B_9408_POSITIVE_PAIR_ROUTES_BOUND",
                "C24A_SOURCE_MEMBER_EXPLICITLY_OUTSIDE_483232_DENOMINATOR",
                "C24A_CURRENT_TARGET_C22_ATOM_JOINED",
                "G2B_PAIR_TERMINAL_IS_POSITIVE_VOLUME_CARRIERS",
                "G2A_ALIAS_ADDS_NO_SECOND_PAIR_OR_INCIDENCE",
                "ALL_483232_ATOMS_HAVE_EXACT_INCIDENCE_SET_OR_EMPTY_COMPLEMENT",
                "ALL_ATOM_PAIR_INCIDENCE_KEYS_ARE_UNIQUE",
                "ALL_INCIDENT_PAIRS_ARE_BOUND_TO_THE_101080_PAIR_AUTHORITY",
                "CURRENT_ONLY_COMPLEMENT_420992_NOT_ACCEPTED_AS_GLOBAL_COMPLEMENT",
            ],
            "prohibited_claims": [
                "ATOM_HAS_AT_MOST_ONE_PAIR",
                "ATOM_HAS_EXACTLY_ONE_TERMINAL",
                "ATOM_TERMINALS_ARE_MUTUALLY_EXCLUSIVE",
            ],
        },
        "unchanged_required_same_chart_authorities": {
            "strict_volume_primitive_rows": 187_132,
            "lower_dimensional_exact_contact_primitive_rows": 5_783_708,
            "C19C_endpoint_v3_half_open_authority_required": True,
            "formal_C24A_G2A_G2B_route_required": True,
            "C26_absence_requires_explicit_primitive_exact_contact_theorem": True,
            "C26_absence_may_not_be_inferred_from_missing_rows_or_volume": True,
        },
        "corrected_acceptance_algorithm": [
            "CAPTURE_ALL_REQUIRED_FORMAL_AUTHORITIES_ON_PINNED_STABLE_DESCRIPTORS",
            "VERIFY_DOCUMENT_AND_ROW_CLOSURES_AND_ZERO_CREDIT",
            "REBUILD_EXACT_20_FAMILY_ROW_KEY_PARTITION_FROM_PRIMITIVE_AUTHORITIES",
            "REBUILD_SAME_CHART_UNION_AND_EXPLICIT_C26_ABSENCE_DISPOSITION",
            "REQUIRE_EXACTLY_ONE_TERMINAL_FOR_EACH_OF_101080_CANDIDATE_PAIRS",
            "REBUILD_EACH_OF_483232_ATOMS_EXACT_DUPLICATE_FREE_PAIR_INCIDENCE_SET",
            "ALLOW_MULTI_PAIR_AND_MULTI_TERMINAL_ATOMS",
            "REQUIRE_EACH_INCIDENCE_PAIR_TO_BIND_THE_UNIQUE_PAIR_TERMINAL",
            "MATERIALIZE_EMPTY_INCIDENCE_SET_AS_EXACT_ATOM_COMPLEMENT",
            "RUN_NO_PRODUCER_IMPORT_VERIFIER_AND_COHERENT_RESIGNED_ATTACKS",
            "RETURN_TRUTHFUL_REJECT_WHILE_ANY_FORMAL_RECEIPT_OR_TOTALITY_CHECK_IS_OPEN",
        ],
        "forbidden_inputs": {
            "old_C27_FAMILIES": True,
            "old_transition_ledger": True,
            "C28_or_C29_as_candidate_authority": True,
            "historical_edge_ledger_as_candidate_universe": True,
        },
        "current_readiness": {
            "scoped_pair_101080_unique_assignment_available": True,
            "full_101080_atom_incidence_formal_receipt_bound_here": False,
            "complete_same_chart_formal_bundle_bound_here": False,
            "primitive_twenty_family_global_totality_proved": False,
            "decision": "REJECT",
        },
        "formal_credit": 0,
        "manifest_authorized": False,
        "strict_nonpromotion": {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    result = dict(body)
    result["design_sha256"] = digest(result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-file", required=True)
    args = parser.parse_args()
    destination = Path(args.out_file)
    try:
        need(not destination.exists(), "fresh correction output")
        result = build()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(canonical(result) + b"\n")
    except (Failure, OSError, TypeError, ValueError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({
        "status": result["status"],
        "design_sha256": result["design_sha256"],
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
