#!/usr/bin/env python3
"""Coherent semantic mutation attacks for the v2 three-terminal blocker."""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


class Rejected(RuntimeError):
    pass


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Rejected(label)


def load_object(path: Path, field: str) -> dict[str, Any]:
    value = json.loads(path.read_bytes())
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body), "object closure")
    return value


def rows(path: Path) -> list[dict[str, Any]]:
    output = []
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for line in stream:
            row = json.loads(line)
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == digest(body), "row closure")
            output.append(row)
    return output


def validate(result: dict[str, Any], route_rows: list[dict[str, Any]],
             blocker_rows: list[dict[str, Any]]) -> None:
    need(result["formal_credit"] == 0, "formal credit")
    need(result["C27_FAMILIES_imported_or_read"] is False, "C27 import")
    need(result["edge_ledger_used_as_candidate_universe"] is False, "edge ledger")
    need(result["C27_C28_C29"] == "REJECT_AND_REBUILD_REQUIRED", "reject")
    surface = result["explicit_upstream_surface"]
    need(surface["SIGNED_distinct_pair_count"] == 25_452, "signed")
    need(surface["COMPLETE_distinct_pair_count"] == 36_140, "complete")
    need(surface["POSITIVE_distinct_member_pair_count"] == 6_322, "positive")
    need(surface["SIGNED_intersection_COMPLETE_pair_count"] == 25_452, "overlap")
    need(surface["SIGNED_is_subset_of_COMPLETE"] is True, "subset")
    need(surface["naturally_mutually_exclusive"] is False, "natural overlap")
    need(surface["priority_rule"] == [
        "SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES",
        "POSITIVE_VOLUME_CARRIERS",
    ], "priority")
    need(surface["priority_disjoint_assignment_census"] == {
        "SIGNED_BOUNDARY_FACES": 25_452,
        "COMPLETE_BOUNDARY_FACES": 10_688,
        "POSITIVE_VOLUME_CARRIERS": 6_322,
    }, "declared assignment")
    need(surface["priority_disjoint_pair_count"] == 42_462, "declared union")
    need(surface["is_total_primitive_candidate_universe"] is False, "surface non-total")
    need(result["current_universe"]["C26_direct_three_terminal_assignment_row_count"] == 0,
         "C26 direct rows")
    need(result["current_universe"]["primitive_atom_count"] == 483_232,
         "primitive atom count")
    blocker = result["minimal_totality_blockers"]
    need(blocker["current_support_rows_requiring_external_chart_or_sign_crosswalk"] == 51_172,
         "chart crosswalk")
    need(blocker["C19C_half_open_atoms_without_row_bound_endpoint_ownership_bits"] == 33_344,
         "endpoint bits")
    need(blocker["R300C_scope_explicitly_nonexhaustive"] is True, "R300C nonexhaustive")
    need(blocker["R300C_nonincident_new_occurrence_count"] == 298_426,
         "R300C nonincident")
    strict = result["strict_nonpromotion"]
    need(strict["the_42462_priority_routed_pairs_are_total_universe"] is False,
         "no total claim")
    need(strict["three_terminal_totality_closed"] is False, "open totality")
    need(strict["C27_transition_totality"] == strict["C28_pair_routing"]
         == strict["C29_physical_maximality"] == 0, "downstream zero")

    seen: set[tuple[str, str]] = set()
    census = Counter()
    signed: set[tuple[str, str]] = set()
    complete: set[tuple[str, str]] = set()
    positive: set[tuple[str, str]] = set()
    for row in route_rows:
        body = dict(row)
        claimed = body.pop("row_sha256", None)
        need(type(claimed) is str and claimed == digest(body), "route closure")
        pair = (row["left_member_id"], row["right_member_id"])
        need(pair[0] < pair[1] and pair not in seen, "route pair")
        seen.add(pair)
        evidence = row["upstream_evidence_multiplicity"]
        if evidence.get("R299_SIGNED_ACCEPTED_FACE", 0) > 0:
            signed.add(pair)
            expected = "SIGNED_BOUNDARY_FACES"
        elif evidence.get("R300B_COMPLETE_ACCEPTED_FACE", 0) > 0:
            expected = "COMPLETE_BOUNDARY_FACES"
        else:
            need(evidence.get("R300C_POSITIVE_VOLUME_WITNESS", 0) > 0,
                 "positive fallback")
            expected = "POSITIVE_VOLUME_CARRIERS"
        if evidence.get("R300B_COMPLETE_ACCEPTED_FACE", 0) > 0:
            complete.add(pair)
        if evidence.get("R300C_POSITIVE_VOLUME_WITNESS", 0) > 0:
            positive.add(pair)
        need(row["assigned_terminal"] == expected, "route terminal")
        census[expected] += 1
    need(len(seen) == 42_462, "route union")
    need(census == surface["priority_disjoint_assignment_census"], "route census")
    need(len(signed) == 25_452 and len(complete) == 36_140, "natural face sets")
    need(signed <= complete and len(signed & complete) == 25_452, "natural overlap")
    need(len(positive) == 6_322 and not (positive & signed) and not (positive & complete),
         "positive disjoint")

    sources = set()
    classes = Counter()
    for row in blocker_rows:
        body = dict(row)
        claimed = body.pop("row_sha256", None)
        need(type(claimed) is str and claimed == digest(body), "blocker closure")
        classes[row["blocker_class"]] += 1
        if "source" in row:
            sources.add(row["source"])
            need(row["row_bound_direct_terminal_assignment_count"] == 0,
                 "blocker direct assignment")
    need(len(blocker_rows) == 7, "blocker count")
    need(sources == {"C19A", "C19B", "C19C", "C20A", "C22A", "C23A"},
         "blocker sources")
    need(classes["EXPLICIT_UPSTREAM_POSITIVE_VOLUME_SCOPE_NONEXHAUSTIVE"] == 1,
         "nonexhaustive blocker")


def reclose(row: dict[str, Any]) -> None:
    row.pop("row_sha256", None)
    row["row_sha256"] = digest(row)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run = Path(args.run_dir)
    base_result = load_object(run / "result.json", "result_sha256")
    base_routes = rows(run / base_result["explicit_upstream_surface"]["route_ledger_filename"])
    base_blockers = rows(run / base_result["minimal_totality_blockers"]["blocker_ledger_filename"])
    validate(base_result, base_routes, base_blockers)

    mutations: list[tuple[str, Callable[[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]], None]]] = [
        ("signed_count", lambda r, q, b: r["explicit_upstream_surface"].__setitem__("SIGNED_distinct_pair_count", 25_451)),
        ("complete_count", lambda r, q, b: r["explicit_upstream_surface"].__setitem__("COMPLETE_distinct_pair_count", 36_139)),
        ("positive_count", lambda r, q, b: r["explicit_upstream_surface"].__setitem__("POSITIVE_distinct_member_pair_count", 6_321)),
        ("overlap_count", lambda r, q, b: r["explicit_upstream_surface"].__setitem__("SIGNED_intersection_COMPLETE_pair_count", 0)),
        ("subset_false", lambda r, q, b: r["explicit_upstream_surface"].__setitem__("SIGNED_is_subset_of_COMPLETE", False)),
        ("natural_exclusive", lambda r, q, b: r["explicit_upstream_surface"].__setitem__("naturally_mutually_exclusive", True)),
        ("priority_reordered", lambda r, q, b: r["explicit_upstream_surface"].__setitem__("priority_rule", list(reversed(r["explicit_upstream_surface"]["priority_rule"])))),
        ("assigned_complete", lambda r, q, b: r["explicit_upstream_surface"]["priority_disjoint_assignment_census"].__setitem__("COMPLETE_BOUNDARY_FACES", 10_689)),
        ("assigned_union", lambda r, q, b: r["explicit_upstream_surface"].__setitem__("priority_disjoint_pair_count", 42_463)),
        ("surface_promoted_total", lambda r, q, b: r["explicit_upstream_surface"].__setitem__("is_total_primitive_candidate_universe", True)),
        ("formal_credit", lambda r, q, b: r.__setitem__("formal_credit", 1)),
        ("C27_import", lambda r, q, b: r.__setitem__("C27_FAMILIES_imported_or_read", True)),
        ("edge_ledger_universe", lambda r, q, b: r.__setitem__("edge_ledger_used_as_candidate_universe", True)),
        ("C27_promoted", lambda r, q, b: r.__setitem__("C27_C28_C29", "PASS")),
        ("totality_closed", lambda r, q, b: r["strict_nonpromotion"].__setitem__("three_terminal_totality_closed", True)),
        ("42462_total", lambda r, q, b: r["strict_nonpromotion"].__setitem__("the_42462_priority_routed_pairs_are_total_universe", True)),
        ("C26_direct_row", lambda r, q, b: r["current_universe"].__setitem__("C26_direct_three_terminal_assignment_row_count", 1)),
        ("atom_census", lambda r, q, b: r["current_universe"].__setitem__("primitive_atom_count", 483_231)),
        ("chart_gap_erased", lambda r, q, b: r["minimal_totality_blockers"].__setitem__("current_support_rows_requiring_external_chart_or_sign_crosswalk", 0)),
        ("endpoint_gap_erased", lambda r, q, b: r["minimal_totality_blockers"].__setitem__("C19C_half_open_atoms_without_row_bound_endpoint_ownership_bits", 0)),
        ("R300C_exhaustive", lambda r, q, b: r["minimal_totality_blockers"].__setitem__("R300C_scope_explicitly_nonexhaustive", False)),
        ("nonincident_erased", lambda r, q, b: r["minimal_totality_blockers"].__setitem__("R300C_nonincident_new_occurrence_count", 0)),
        ("route_terminal_flip", lambda r, q, b: (q[0].__setitem__("assigned_terminal", "POSITIVE_VOLUME_CARRIERS"), reclose(q[0]))),
        ("route_pair_reverse", lambda r, q, b: (q[0].__setitem__("left_member_id", q[0]["right_member_id"]), reclose(q[0]))),
        ("blocker_assignment_forged", lambda r, q, b: (b[0].__setitem__("row_bound_direct_terminal_assignment_count", 1), reclose(b[0]))),
    ]
    outcomes = []
    for name, mutate in mutations:
        result = deepcopy(base_result)
        routes = deepcopy(base_routes)
        blockers = deepcopy(base_blockers)
        mutate(result, routes, blockers)
        rejected = False
        reason = None
        try:
            validate(result, routes, blockers)
        except Rejected as error:
            rejected = True
            reason = str(error)
        need(rejected, "attack accepted:" + name)
        outcomes.append({"attack": name, "rejected": True, "reason": reason})
    value: dict[str, Any] = {
        "all_rejected": True,
        "attack_count": len(outcomes),
        "attacks": outcomes,
        "formal_credit": 0,
        "status": "PASS_25_OF_25_COHERENT_MUTATIONS_REJECTED__ZERO_CREDIT",
    }
    value["result_sha256"] = digest(value)
    Path(args.output).write_bytes(canonical(value) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Rejected as error:
        print("FAIL:" + str(error))
        raise SystemExit(2)
