#!/usr/bin/env python3
"""Emit the zero-credit, fail-closed v5 twenty-family aggregator contract.

This design emitter reads no evidence.  It records the primitive authorities
that a future aggregator must capture and the checks it must perform before it
may return anything other than truthful REJECT.
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
        "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-aggregator-design.v1",
        "status": "DESIGN_READY__FORMAL_AUTHORITIES_INCOMPLETE__TRUTHFUL_REJECT__ZERO_CREDIT",
        "execution_policy": {
            "default_decision": "REJECT",
            "missing_required_receipt_decision": "REJECT_MISSING_FORMAL_AUTHORITY",
            "invalid_closure_or_pin_decision": "REJECT_INVALID_AUTHORITY",
            "census_or_key_mismatch_decision": "REJECT_SEMANTIC_MISMATCH",
            "atom_totality_or_exclusivity_open_decision": "REJECT_GLOBAL_TOTALITY_OPEN",
            "promotion_on_partial_evidence_forbidden": True,
            "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat_required": True,
            "producer_module_import_forbidden": True,
        },
        "forbidden_inputs": {
            "old_C27_FAMILIES": True,
            "old_transition_ledger": True,
            "C28_as_candidate_authority": True,
            "C29_as_candidate_authority": True,
            "historical_edge_ledger_as_candidate_universe": True,
        },
        "required_authority_slots": {
            "primitive_twenty_family_registry": {
                "required": True,
                "requirements": [
                    "EXACTLY_20_PRIMITIVE_FAMILY_KEYS",
                    "ROW_BOUND_FAMILY_MEMBERSHIP",
                    "PAIRWISE_MUTUAL_EXCLUSIVITY",
                    "EXHAUSTIVENESS_ON_DECLARED_PRIMITIVE_DENOMINATOR",
                    "NO_C27_FAMILIES_OR_TRANSITION_IMPORT",
                ],
            },
            "same_chart_strict_volume": {
                "required": True,
                "expected_primitive_row_count": 187_132,
                "role": "SAME_CHART_STRICT_VOLUME_AUTHORITY",
                "formal_receipt_required": True,
            },
            "same_chart_lower_dimensional_exact_contact": {
                "required": True,
                "expected_primitive_row_count": 5_783_708,
                "role": "SAME_CHART_LOWER_DIMENSIONAL_EXACT_CONTACT_AUTHORITY",
                "formal_receipt_required": True,
            },
            "C19C_endpoint_v3_half_open": {
                "required": True,
                "required_schema": "cm2.c19c-endpoint-ownership-v3.terminal-receipt.v1",
                "role": "HALF_OPEN_FACE_AND_JUNCTION_OWNERSHIP_AUTHORITY",
                "must_remain_zero_credit": True,
            },
            "formal_C24A_G2A_G2B_route": {
                "required": True,
                "requirements": [
                    "G2A_SOURCE_EXEC_BOUND_SCOPED_AUTHORITY",
                    "G2B_TERMINAL_AUTHORITY",
                    "9408_POSITIVE_KEY_BIJECTION",
                    "9392_REVERSE_EMPTY_KEY_BIJECTION",
                    "G2A_GRAPH_ALIAS_NOT_SECOND_CANDIDATE",
                    "G2B_POSITIVE_ASSIGNED_TO_POSITIVE_VOLUME_CARRIERS",
                ],
            },
            "C26_primitive_exact_contact_absence": {
                "required": True,
                "role": "EXPLICIT_THEOREM_NOT_MISSING_ROW_INFERENCE",
                "requirements": [
                    "C26_SCOPE_ENUMERATED_BY_PRIMITIVE_EXACT_CONTACT_THEOREM",
                    "ZERO_C26_CONTACT_DISPOSITION_EXPLICITLY_PROVED",
                    "ABSENCE_NOT_INFERRED_FROM_EMPTY_OUTPUT_OR_VOLUME",
                    "THEOREM_ROWS_BOUND_TO_LOWER_DIMENSIONAL_DENOMINATOR",
                ],
            },
            "full_101080_three_terminal_atom_incidence": {
                "required": True,
                "pair_ownership_row_count": 101_080,
                "primitive_support_atom_denominator": 483_232,
                "requirements": [
                    "CURRENT_91672_PAIR_ROUTES_BOUND",
                    "C24A_G2B_9408_POSITIVE_PAIR_ROUTES_BOUND",
                    "C24A_SOURCE_MEMBER_EXPLICITLY_OUTSIDE_483232_DENOMINATOR",
                    "C24A_CURRENT_TARGET_C22_ATOM_JOINED",
                    "G2B_TERMINAL_IS_POSITIVE_VOLUME_CARRIERS",
                    "G2A_ALIAS_ADDS_NO_SECOND_ATOM_OR_PAIR_ASSIGNMENT",
                    "EVERY_DENOMINATOR_ATOM_HAS_ZERO_OR_ONE_PAIR_INCIDENCE",
                    "EVERY_INCIDENT_ATOM_HAS_EXACTLY_ONE_TERMINAL",
                    "NONINCIDENT_COMPLEMENT_EXACTLY_MATERIALIZED",
                    "CURRENT_ONLY_COMPLEMENT_420992_NOT_ACCEPTED_AS_GLOBAL_COMPLEMENT",
                ],
                "terminal_priority": [
                    "SIGNED_BOUNDARY_FACES",
                    "COMPLETE_BOUNDARY_FACES",
                    "POSITIVE_VOLUME_CARRIERS",
                ],
            },
        },
        "same_chart_aggregation_contract": {
            "required_bound_inputs": [
                "STRICT_VOLUME_187132",
                "LOWER_DIMENSIONAL_EXACT_CONTACT_5783708",
                "C19C_ENDPOINT_V3_HALF_OPEN",
                "FORMAL_C24A_G2A_G2B_ROUTE",
                "C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_THEOREM",
            ],
            "set_operation": "UNION_BY_PRIMITIVE_ROW_BOUND_KEY_THEN_REQUIRE_UNIQUE_OWNER",
            "volume_used_to_infer_face_or_C26_contact": False,
            "G2A_G2B_alias_double_count_forbidden": True,
        },
        "three_terminal_aggregation_contract": {
            "required_bound_input": "FULL_101080_THREE_TERMINAL_ATOM_INCIDENCE",
            "pair_layer_scoped_union_count": 101_080,
            "pair_layer_scoped_unique_assignment_is_not_atom_totality": True,
            "atom_layer_exhaustive_and_mutually_exclusive_selection_required": True,
            "pair_routing_totality_on_483232_denominator_required": True,
        },
        "acceptance_algorithm": [
            "CAPTURE_ALL_REQUIRED_AUTHORITY_FILES_ON_PINNED_STABLE_DESCRIPTORS",
            "VERIFY_DOCUMENT_AND_ROW_CLOSURES_AND_FORMAL_ZERO_CREDIT",
            "REBUILD_EXACT_20_FAMILY_ROW_KEY_PARTITION_FROM_PRIMITIVE_AUTHORITIES",
            "REBUILD_SAME_CHART_UNION_AND_C26_EXPLICIT_ABSENCE_DISPOSITION",
            "REBUILD_FULL_101080_ATOM_TO_PAIR_INCIDENCE_AND_COMPLEMENT",
            "REQUIRE_ONE_TERMINAL_PER_INCIDENT_ATOM_AND_NO_G2A_G2B_DOUBLE_COUNT",
            "RUN_NO_PRODUCER_IMPORT_INDEPENDENT_VERIFIER_AND_COHERENT_ATTACKS",
            "RETURN_SCOPED_PASS_ONLY_IF_ALL_REQUIRED_RECEIPTS_ARE_FORMAL_AND_VALID",
        ],
        "current_readiness": {
            "pair_layer_101080_scoped_comparator_available": True,
            "pair_layer_independent_verifier_available": True,
            "pair_layer_coherent_attacks_available": True,
            "full_101080_atom_incidence_formal_receipt_available_to_this_design": False,
            "complete_same_chart_formal_receipt_bundle_available_to_this_design": False,
            "primitive_twenty_family_global_totality_available": False,
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
        need(not destination.exists(), "fresh design output")
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
