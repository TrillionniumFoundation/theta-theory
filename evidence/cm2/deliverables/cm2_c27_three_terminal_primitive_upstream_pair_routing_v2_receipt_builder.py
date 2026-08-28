#!/usr/bin/env python3
"""Publish a zero-credit receipt for the v2 three-terminal blocker audit."""

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
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def closed(path: Path, field: str) -> dict[str, Any]:
    raw = path.read_bytes()
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw,
         "canonical object:" + str(path))
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body),
         "object closure:" + str(path))
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-a", required=True)
    parser.add_argument("--run-b", required=True)
    parser.add_argument("--producer", required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--attacks", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    runs = [Path(args.run_a), Path(args.run_b)]
    producer = Path(args.producer)
    verifier = Path(args.verifier)
    attacks = Path(args.attacks)
    producer_sha = file_hash(producer)
    verifier_sha = file_hash(verifier)
    attacks_sha = file_hash(attacks)

    results = [closed(run / "result.json", "result_sha256") for run in runs]
    verifications = [
        closed(run / "independent_verification.json", "verification_sha256")
        for run in runs
    ]
    attack_results = [
        closed(run / "attack_result.json", "result_sha256") for run in runs
    ]
    for result in results:
        need(
            result["status"]
            == "PASS_EXPLICIT_UPSTREAM_SURFACE_PRIORITY_ROUTING_25452_10688_6322__REJECT_PRIMITIVE_FULL_SUPPORT_TOTALITY__ZERO_CREDIT"
            and result["formal_credit"] == 0
            and result["C27_FAMILIES_imported_or_read"] is False
            and result["edge_ledger_used_as_candidate_universe"] is False
            and result["C27_C28_C29"] == "REJECT_AND_REBUILD_REQUIRED"
            and result["CM2"] == "NO-GO_FOR_CLAIM",
            "producer fail-closed result",
        )
    need(
        results[0]["invocation_seed"] != results[1]["invocation_seed"]
        and results[0]["semantic_projection_sha256"]
        == results[1]["semantic_projection_sha256"],
        "real double seed semantic identity",
    )
    route_name = results[0]["explicit_upstream_surface"]["route_ledger_filename"]
    blocker_name = results[0]["minimal_totality_blockers"]["blocker_ledger_filename"]
    need(
        (runs[0] / route_name).read_bytes() == (runs[1] / route_name).read_bytes()
        and (runs[0] / blocker_name).read_bytes() == (runs[1] / blocker_name).read_bytes(),
        "double-seed ledger byte identity",
    )
    for run, result, verification, attack in zip(
        runs, results, verifications, attack_results
    ):
        need(
            verification["status"]
            == "PASS_INDEPENDENT_EXPLICIT_SURFACE_ROUTING__REJECT_FULL_SUPPORT_TOTALITY__ZERO_CREDIT"
            and verification["producer_file_sha256"] == producer_sha
            and verification["result_file_sha256"] == file_hash(run / "result.json")
            and verification["result_sha256"] == result["result_sha256"]
            and verification["route_pair_count"] == 42_462
            and verification["SIGNED_COMPLETE_overlap_pair_count"] == 25_452
            and verification["blocker_row_count"] == 7
            and verification["explicit_surface_is_total_universe"] is False
            and verification["formal_credit"] == 0,
            "independent verification",
        )
        need(
            attack["status"]
            == "PASS_25_OF_25_COHERENT_MUTATIONS_REJECTED__ZERO_CREDIT"
            and attack["attack_count"] == 25
            and attack["all_rejected"] is True
            and attack["formal_credit"] == 0,
            "coherent attacks",
        )
    need(
        (runs[0] / "attack_result.json").read_bytes()
        == (runs[1] / "attack_result.json").read_bytes(),
        "double-seed attack-result identity",
    )

    surface = results[0]["explicit_upstream_surface"]
    blockers = results[0]["minimal_totality_blockers"]
    receipt: dict[str, Any] = {
        "schema": "cm2.c27-independent.three-terminal-primitive-upstream-pair-routing-v2.blocker-receipt.v1",
        "status": "PASS_EXPLICIT_UPSTREAM_SURFACE_UNIQUE_PRIORITY_ROUTING__REJECT_TOTALITY__ZERO_CREDIT",
        "producer_sha256": producer_sha,
        "independent_verifier_sha256": verifier_sha,
        "attack_harness_sha256": attacks_sha,
        "double_seed": {
            "seeds": [results[0]["invocation_seed"], results[1]["invocation_seed"]],
            "semantic_projection_identical": True,
            "route_ledger_byte_identical": True,
            "blocker_ledger_byte_identical": True,
            "attack_result_byte_identical": True,
        },
        "explicit_upstream_surface": {
            "SIGNED_pair_count": surface["SIGNED_distinct_pair_count"],
            "COMPLETE_pair_count": surface["COMPLETE_distinct_pair_count"],
            "POSITIVE_member_pair_count": surface["POSITIVE_distinct_member_pair_count"],
            "SIGNED_is_subset_of_COMPLETE": True,
            "SIGNED_COMPLETE_overlap_pair_count": surface["SIGNED_intersection_COMPLETE_pair_count"],
            "naturally_mutually_exclusive": False,
            "declared_priority": surface["priority_rule"],
            "priority_disjoint_assignment_census": surface["priority_disjoint_assignment_census"],
            "priority_disjoint_pair_count": surface["priority_disjoint_pair_count"],
            "C15_C25_endpoint_crosswalk_gap": 0,
            "all_routed_pairs_already_same_current_C15_component": (
                surface["routed_pair_cross_current_C15_component_count"] == 0
            ),
            "is_total_primitive_candidate_universe": False,
            "route_ledger_file_sha256": surface["route_ledger_file_sha256"],
            "route_ledger_rows_sha256": surface["route_ledger_rows_sha256"],
        },
        "minimal_totality_blockers": {
            "C26_direct_three_terminal_assignment_row_count": 0,
            "primitive_atoms_without_direct_terminal_binding": blockers["primitive_atoms_without_direct_terminal_binding"],
            "current_support_rows_requiring_external_chart_or_sign_crosswalk": blockers["current_support_rows_requiring_external_chart_or_sign_crosswalk"],
            "C19C_half_open_atoms_without_row_bound_endpoint_ownership_bits": blockers["C19C_half_open_atoms_without_row_bound_endpoint_ownership_bits"],
            "R300C_scope_explicitly_nonexhaustive": True,
            "R300C_nonincident_new_occurrence_count": blockers["R300C_nonincident_new_occurrence_count"],
            "R300C_withheld_Round248_wall_sheet_count": blockers["R300C_withheld_Round248_wall_sheet_count"],
            "R300C_withheld_inherited_2D_sheet_count": blockers["R300C_withheld_inherited_2D_sheet_count"],
            "blocker_ledger_file_sha256": blockers["blocker_ledger_file_sha256"],
            "blocker_ledger_rows_sha256": blockers["blocker_ledger_rows_sha256"],
        },
        "attack_harness": {
            "attack_count": 25,
            "all_rejected": True,
            "result_file_sha256": file_hash(runs[0] / "attack_result.json"),
            "result_sha256": attack_results[0]["result_sha256"],
        },
        "strict_nonpromotion": {
            "the_42462_priority_routed_pairs_are_total_universe": False,
            "three_terminal_totality_closed": False,
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
        },
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    receipt["receipt_sha256"] = digest(receipt)
    Path(args.output).write_bytes(canonical(receipt) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("FAIL:" + str(error))
        raise SystemExit(2)
