#!/usr/bin/env python3
"""Independent structural verifier for the v2 three-terminal blocker audit."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Iterator


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


def closed_object(path: Path, field: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and raw.count(b"\n") == 1,
         "single canonical object:" + str(path))
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw,
         "canonical object:" + str(path))
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body),
         "object closure:" + str(path))
    return value


def gzip_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, line in enumerate(stream):
            need(line.endswith(b"\n"), f"newline:{path}:{ordinal}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw,
                 f"canonical row:{path}:{ordinal}")
            body = dict(row)
            claimed = body.pop("row_sha256", None)
            need(type(claimed) is str and claimed == digest(body),
                 f"row closure:{path}:{ordinal}")
            yield row


def rows_digest(path: Path) -> tuple[str, int]:
    state = hashlib.sha256()
    count = 0
    for row in gzip_rows(path):
        state.update(canonical(row))
        count += 1
    return state.hexdigest(), count


def verify(run_dir: Path, producer_path: Path) -> dict[str, Any]:
    result_path = run_dir / "result.json"
    result = closed_object(result_path, "result_sha256")
    need(
        result["status"]
        == "PASS_EXPLICIT_UPSTREAM_SURFACE_PRIORITY_ROUTING_25452_10688_6322__REJECT_PRIMITIVE_FULL_SUPPORT_TOTALITY__ZERO_CREDIT",
        "result status",
    )
    need(
        result["C27_FAMILIES_imported_or_read"] is False
        and result["edge_ledger_used_as_candidate_universe"] is False
        and result["formal_credit"] == 0
        and result["C27_C28_C29"] == "REJECT_AND_REBUILD_REQUIRED"
        and result["CM2"] == "NO-GO_FOR_CLAIM",
        "strict top-level fail close",
    )
    surface = result["explicit_upstream_surface"]
    need(
        surface["SIGNED_distinct_pair_count"] == 25_452
        and surface["COMPLETE_distinct_pair_count"] == 36_140
        and surface["POSITIVE_distinct_member_pair_count"] == 6_322
        and surface["SIGNED_intersection_COMPLETE_pair_count"] == 25_452
        and surface["SIGNED_is_subset_of_COMPLETE"] is True
        and surface["POSITIVE_intersection_SIGNED_pair_count"] == 0
        and surface["POSITIVE_intersection_COMPLETE_pair_count"] == 0
        and surface["naturally_mutually_exclusive"] is False
        and surface["priority_rule"] == [
            "SIGNED_BOUNDARY_FACES",
            "COMPLETE_BOUNDARY_FACES",
            "POSITIVE_VOLUME_CARRIERS",
        ]
        and surface["priority_disjoint_assignment_census"] == {
            "COMPLETE_BOUNDARY_FACES": 10_688,
            "POSITIVE_VOLUME_CARRIERS": 6_322,
            "SIGNED_BOUNDARY_FACES": 25_452,
        }
        and surface["priority_disjoint_pair_count"] == 42_462
        and surface["route_endpoint_C15_C25_crosswalk_gap"] == 0
        and surface["is_total_primitive_candidate_universe"] is False,
        "surface census and non-totality",
    )

    route_path = run_dir / surface["route_ledger_filename"]
    need(file_hash(route_path) == surface["route_ledger_file_sha256"],
         "route file hash")
    route_rows_state = hashlib.sha256()
    assigned = Counter()
    seen: set[tuple[str, str]] = set()
    natural_signed: set[tuple[str, str]] = set()
    natural_complete: set[tuple[str, str]] = set()
    natural_positive: set[tuple[str, str]] = set()
    same_component = 0
    cross_component = 0
    for row in gzip_rows(route_path):
        route_rows_state.update(canonical(row))
        pair = (row["left_member_id"], row["right_member_id"])
        need(pair[0] < pair[1] and pair not in seen, "ordered unique route pair")
        seen.add(pair)
        evidence = row["upstream_evidence_multiplicity"]
        need(type(evidence) is dict and bool(evidence), "route evidence")
        if evidence.get("R299_SIGNED_ACCEPTED_FACE", 0) > 0:
            natural_signed.add(pair)
            expected = "SIGNED_BOUNDARY_FACES"
        elif evidence.get("R300B_COMPLETE_ACCEPTED_FACE", 0) > 0:
            expected = "COMPLETE_BOUNDARY_FACES"
        else:
            need(evidence.get("R300C_POSITIVE_VOLUME_WITNESS", 0) > 0,
                 "positive evidence fallback")
            expected = "POSITIVE_VOLUME_CARRIERS"
        if evidence.get("R300B_COMPLETE_ACCEPTED_FACE", 0) > 0:
            natural_complete.add(pair)
        if evidence.get("R300C_POSITIVE_VOLUME_WITNESS", 0) > 0:
            natural_positive.add(pair)
        need(
            row["assigned_terminal"] == expected
            and row["pair_assignment_rule"]
            == "FIRST_MATCH_SIGNED_THEN_COMPLETE_THEN_POSITIVE"
            and row["upstream_surface_only_not_total_universe"] is True,
            "exact priority assignment",
        )
        components = row["current_C15_components"]
        need(type(components) is list and len(components) == 2,
             "two current components")
        if components[0] == components[1]:
            same_component += 1
        else:
            cross_component += 1
        assigned[expected] += 1
    need(
        len(seen) == 42_462
        and assigned == {
            "SIGNED_BOUNDARY_FACES": 25_452,
            "COMPLETE_BOUNDARY_FACES": 10_688,
            "POSITIVE_VOLUME_CARRIERS": 6_322,
        }
        and len(natural_signed) == 25_452
        and len(natural_complete) == 36_140
        and natural_signed <= natural_complete
        and len(natural_signed & natural_complete) == 25_452
        and len(natural_positive) == 6_322
        and not (natural_positive & natural_signed)
        and not (natural_positive & natural_complete),
        "independent route reconstruction",
    )
    need(
        route_rows_state.hexdigest() == surface["route_ledger_rows_sha256"]
        and same_component == surface["routed_pair_same_current_C15_component_count"]
        and cross_component == surface["routed_pair_cross_current_C15_component_count"],
        "route commitments",
    )

    blockers = result["minimal_totality_blockers"]
    need(
        blockers["all_483232_primitive_atoms_have_direct_terminal_binding"] is False
        and blockers["primitive_atoms_without_direct_terminal_binding"] == 483_232
        and blockers["current_support_rows_requiring_external_chart_or_sign_crosswalk"] == 51_172
        and blockers["C19C_half_open_atoms_without_row_bound_endpoint_ownership_bits"] == 33_344
        and blockers["R300C_scope_explicitly_nonexhaustive"] is True
        and blockers["R300C_nonincident_new_occurrence_count"] == 298_426
        and blockers["R300C_withheld_Round248_wall_sheet_count"] == 38_360
        and blockers["R300C_withheld_inherited_2D_sheet_count"] == 264,
        "exact blocker census",
    )
    blocker_path = run_dir / blockers["blocker_ledger_filename"]
    need(file_hash(blocker_path) == blockers["blocker_ledger_file_sha256"],
         "blocker file hash")
    blocker_rows_state = hashlib.sha256()
    blocker_classes = Counter()
    sources: set[str] = set()
    blocker_count = 0
    for row in gzip_rows(blocker_path):
        blocker_rows_state.update(canonical(row))
        blocker_count += 1
        blocker_classes[row["blocker_class"]] += 1
        if "source" in row:
            sources.add(row["source"])
            need(row["row_bound_direct_terminal_assignment_count"] == 0,
                 "source direct terminal gap")
    need(
        blocker_count == 7
        and sources == {"C19A", "C19B", "C19C", "C20A", "C22A", "C23A"}
        and blocker_classes
        == {
            "CURRENT_PRIMITIVE_FULL_SUPPORT_TO_THREE_TERMINAL_PAIR_SELECTION_CROSSWALK_ABSENT": 6,
            "EXPLICIT_UPSTREAM_POSITIVE_VOLUME_SCOPE_NONEXHAUSTIVE": 1,
        }
        and blocker_rows_state.hexdigest() == blockers["blocker_ledger_rows_sha256"],
        "blocker ledger reconstruction",
    )

    strict = result["strict_nonpromotion"]
    need(
        strict
        == {
            "C27_transition_totality": 0,
            "C28_pair_routing": 0,
            "C29_physical_maximality": 0,
            "the_42462_priority_routed_pairs_are_total_universe": False,
            "three_terminal_totality_closed": False,
            "unique_assignment_closed_for_explicit_upstream_surface_only": True,
        },
        "strict nonpromotion object",
    )
    verification: dict[str, Any] = {
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
        "formal_credit": 0,
        "producer_file_sha256": file_hash(producer_path),
        "result_file_sha256": file_hash(result_path),
        "result_sha256": result["result_sha256"],
        "route_ledger_file_sha256": file_hash(route_path),
        "route_pair_count": len(seen),
        "route_assignment_census": dict(sorted(assigned.items())),
        "SIGNED_COMPLETE_overlap_pair_count": len(natural_signed & natural_complete),
        "blocker_ledger_file_sha256": file_hash(blocker_path),
        "blocker_row_count": blocker_count,
        "explicit_surface_is_total_universe": False,
        "status": "PASS_INDEPENDENT_EXPLICIT_SURFACE_ROUTING__REJECT_FULL_SUPPORT_TOTALITY__ZERO_CREDIT",
    }
    verification["verification_sha256"] = digest(verification)
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--producer", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    value = verify(Path(args.run_dir), Path(args.producer))
    Path(args.output).write_bytes(canonical(value) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print("FAIL:" + str(error))
        raise SystemExit(2)
