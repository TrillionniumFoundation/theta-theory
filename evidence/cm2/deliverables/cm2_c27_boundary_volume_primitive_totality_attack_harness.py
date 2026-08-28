#!/usr/bin/env python3
"""Coherent mutation attacks for the boundary/volume primitive REJECT gate."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


EXPECTED_SOURCES = {
    "C19A": 5_596, "C19B": 12_232, "C19C": 33_344,
    "C20A": 126_468, "C22A": 295_340, "C23A": 10_252,
}
MISSING_BITS = [
    "axis_0_lower_included", "axis_0_upper_included",
    "axis_1_lower_included", "axis_1_upper_included",
    "axis_2_lower_included", "axis_2_upper_included",
]
TERMINALS = [
    "SIGNED_BOUNDARY_FACES", "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS",
]


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


def object_from_file(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and b"\n" not in raw[:-1], "single canonical JSON")
    value = json.loads(raw[:-1])
    need(type(value) is dict and canonical(value) + b"\n" == raw, "canonical result")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "result closure")
    return value


def ledger_rows(path: Path) -> tuple[list[dict[str, Any]], str]:
    output: list[dict[str, Any]] = []
    state = hashlib.sha256()
    with gzip.open(path, "rb") as stream:
        for line_number, line in enumerate(stream, 1):
            need(line.endswith(b"\n"), f"ledger newline:{line_number}")
            raw = line[:-1]
            row = json.loads(raw)
            need(type(row) is dict and canonical(row) == raw, f"ledger canonical:{line_number}")
            state.update(raw)
            output.append(row)
    return output, state.hexdigest()


def validate_result(value: dict[str, Any]) -> None:
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(body), "candidate closure")
    universe = value["primitive_atom_universe"]
    faces = value["boundary_face_census"]
    volume = value["positive_volume_census"]
    missing = value["minimal_missing_authority"]
    c26 = value["C26_audit"]
    need(universe["source_census"] == EXPECTED_SOURCES, "source census")
    need(universe["atom_count"] == 483_232, "atom count")
    need(universe["distinct_owner_member_count"] == 482_380, "owner count")
    need(universe["C15_member_component_join_gap"] == 0 and
         universe["C25_typed_support_join_gap"] == 0, "join gaps")
    need(volume["positive_coordinate_volume_atom_count"] == 483_232 and
         volume["nonpositive_coordinate_volume_atom_count"] == 0 and
         volume["exact_volume_field_verified_count"] == 177_640 and
         volume["T2PS_positive_physical_measure_via_analytic_branch_count"] == 10_252,
         "volume census")
    need(volume["terminal_totality_state"].startswith("REJECT_"), "volume reject")
    need(faces["geometric_oriented_face_count"] == 2_899_392 and
         faces["positive_coordinate_area_face_count"] == 2_899_392 and
         faces["geometric_outward_orientation_sign_known_count"] == 2_899_392,
         "geometric face census")
    need(faces["open_interval_explicitly_excluded_face_count"] == 2_699_328 and
         faces["half_open_endpoint_membership_unknown_face_count"] == 200_064,
         "face membership partition")
    need(faces["support_factor_or_predicate_signed_face_authority_count"] == 0 and
         faces["support_factor_or_predicate_signed_face_authority_gap_count"] == 2_899_392,
         "signed authority gap")
    endpoint = missing["half_open_endpoint_ownership"]
    need(endpoint["atom_count"] == 33_344 and endpoint["face_bit_count"] == 200_064 and
         endpoint["missing_fields"] == MISSING_BITS, "endpoint gap")
    assignment = missing["three_terminal_selection"]
    need(assignment["affected_atom_count"] == 483_232 and
         assignment["assigned_atom_count"] == 0 and
         assignment["terminal_names"] == TERMINALS, "assignment gap")
    need(c26["feature_count"] == 691_424 and
         c26["C22A_R1_exact_source_row_cover_count"] == 295_340 and
         c26["direct_boundary_or_volume_terminal_assignment_row_count"] == 0 and
         c26["atoms_without_direct_boundary_or_volume_terminal_assignment_row_count"] == 483_232,
         "C26 fail-close")
    need(set(value["terminal_states"]) == set(TERMINALS) and
         all(state.startswith("REJECT_") for state in value["terminal_states"].values()),
         "terminal reject states")
    need(value["formal_credit"] == 0 and value["C27_C28_C29"] == "REJECT" and
         value["CM2"] == "NO-GO_FOR_CLAIM" and
         value["C27_FAMILIES_imported_or_read"] is False and
         value["edge_ledger_used_as_candidate_universe"] is False,
         "strict nonpromotion")


def validate_ledger(rows: list[dict[str, Any]], expected_rows_sha256: str) -> None:
    need(len(rows) == 33_344, "ledger count")
    ids: set[str] = set()
    state = hashlib.sha256()
    for row in rows:
        body = dict(row)
        claimed = body.pop("row_sha256", None)
        need(type(claimed) is str and claimed == digest(body), "ledger row closure")
        need(row["source"] == "C19C", "ledger source")
        need(row["atom_id"] == "C19C:" + row["source_row_sha256"], "atom identity")
        need(row["atom_id"] not in ids, "unique atom")
        ids.add(row["atom_id"])
        need(type(row["member_id"]) is str and row["member_id"] != "", "member")
        need(type(row["fresh_component_id"]) is str and row["fresh_component_id"] != "", "component")
        need(len(row["bounds"]) == 6, "six bounds")
        need(row["missing_endpoint_ownership_fields"] == MISSING_BITS, "six missing bits")
        need(row["minimal_missing_authority"] ==
             "ROW_BOUND_SIX_ENDPOINT_OWNERSHIP_BITS_OR_AN_EQUIVALENT_HALF_OPEN_PARTITION_RULE",
             "minimal authority")
        state.update(canonical(row))
    need(state.hexdigest() == expected_rows_sha256, "ledger sequence commitment")


def reclose(value: dict[str, Any]) -> dict[str, Any]:
    value.pop("result_sha256", None)
    value["result_sha256"] = digest(value)
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    candidate_path = Path(args.candidate)
    ledger_path = Path(args.ledger)
    candidate = object_from_file(candidate_path)
    rows, rows_sha = ledger_rows(ledger_path)
    need(file_hash(ledger_path) == candidate["minimal_missing_authority"]["half_open_endpoint_ownership"]["ledger_file_sha256"],
         "ledger file pin")
    need(rows_sha == candidate["minimal_missing_authority"]["half_open_endpoint_ownership"]["ledger_rows_sha256"],
         "ledger rows pin")
    validate_result(candidate)
    validate_ledger(rows, rows_sha)

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("atom_count", lambda d: d["primitive_atom_universe"].__setitem__("atom_count", 483_231)),
        ("source_census", lambda d: d["primitive_atom_universe"]["source_census"].__setitem__("C19C", 33_343)),
        ("owner_count", lambda d: d["primitive_atom_universe"].__setitem__("distinct_owner_member_count", 482_381)),
        ("positive_count", lambda d: d["positive_volume_census"].__setitem__("positive_coordinate_volume_atom_count", 483_231)),
        ("nonpositive_count", lambda d: d["positive_volume_census"].__setitem__("nonpositive_coordinate_volume_atom_count", 1)),
        ("volume_promoted", lambda d: d["positive_volume_census"].__setitem__("terminal_totality_state", "PASS_CLOSED")),
        ("face_count", lambda d: d["boundary_face_census"].__setitem__("geometric_oriented_face_count", 2_899_391)),
        ("open_face_count", lambda d: d["boundary_face_census"].__setitem__("open_interval_explicitly_excluded_face_count", 2_699_327)),
        ("half_open_face_count", lambda d: d["boundary_face_census"].__setitem__("half_open_endpoint_membership_unknown_face_count", 200_063)),
        ("signed_authority_forged", lambda d: d["boundary_face_census"].__setitem__("support_factor_or_predicate_signed_face_authority_count", 1)),
        ("endpoint_atom_count", lambda d: d["minimal_missing_authority"]["half_open_endpoint_ownership"].__setitem__("atom_count", 33_343)),
        ("assignment_forged", lambda d: d["minimal_missing_authority"]["three_terminal_selection"].__setitem__("assigned_atom_count", 1)),
        ("C26_assignment_forged", lambda d: d["C26_audit"].__setitem__("direct_boundary_or_volume_terminal_assignment_row_count", 1)),
        ("terminal_promoted", lambda d: d["terminal_states"].__setitem__("COMPLETE_BOUNDARY_FACES", "PASS_CLOSED")),
        ("formal_credit", lambda d: d.__setitem__("formal_credit", 1)),
        ("C27_promoted", lambda d: d.__setitem__("C27_C28_C29", "PASS")),
        ("CM2_promoted", lambda d: d.__setitem__("CM2", "GO")),
        ("FAMILIES_read_flip", lambda d: d.__setitem__("C27_FAMILIES_imported_or_read", True)),
        ("edge_ledger_flip", lambda d: d.__setitem__("edge_ledger_used_as_candidate_universe", True)),
    ]
    rejected: list[str] = []
    for attack_id, mutate in mutations:
        changed = copy.deepcopy(candidate)
        mutate(changed)
        reclose(changed)
        try:
            validate_result(changed)
        except (Failure, KeyError, TypeError, ValueError):
            rejected.append(attack_id)
            continue
        raise Failure("accepted result mutation:" + attack_id)

    row_attacks: list[tuple[str, Callable[[list[dict[str, Any]]], None]]] = [
        ("ledger_drop", lambda d: d.pop()),
        ("ledger_duplicate", lambda d: d.__setitem__(-1, copy.deepcopy(d[0]))),
        ("ledger_missing_bit", lambda d: d[0]["missing_endpoint_ownership_fields"].pop()),
        ("ledger_source_flip", lambda d: d[0].__setitem__("source", "C19B")),
        ("ledger_member_empty", lambda d: d[0].__setitem__("member_id", "")),
        ("ledger_component_empty", lambda d: d[0].__setitem__("fresh_component_id", "")),
        ("ledger_bounds_drop", lambda d: d[0]["bounds"].pop()),
        ("ledger_atom_identity_flip", lambda d: d[0].__setitem__("atom_id", "C19C:" + "0" * 64)),
    ]
    for attack_id, mutate in row_attacks:
        changed = list(rows)
        changed[0] = copy.deepcopy(changed[0])
        mutate(changed)
        if changed and isinstance(changed[0], dict):
            changed[0].pop("row_sha256", None)
            changed[0]["row_sha256"] = digest(changed[0])
        try:
            validate_ledger(changed, rows_sha)
        except (Failure, KeyError, TypeError, ValueError):
            rejected.append(attack_id)
            continue
        raise Failure("accepted ledger mutation:" + attack_id)

    attack_count = len(mutations) + len(row_attacks)
    need(len(rejected) == attack_count, "all attacks rejected")
    result = {
        "all_rejected": True,
        "attack_count": attack_count,
        "candidate_file_sha256": file_hash(candidate_path),
        "candidate_result_sha256": candidate["result_sha256"],
        "formal_credit": 0,
        "ledger_file_sha256": file_hash(ledger_path),
        "ledger_rows_sha256": rows_sha,
        "rejected_attack_ids": rejected,
        "rejected_count": len(rejected),
        "status": "PASS_27_OF_27_COHERENT_MUTATIONS_REJECTED__TRUTHFUL_THREE_TERMINAL_REJECT_PRESERVED__ZERO_CREDIT",
    }
    result["result_sha256"] = digest(result)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_bytes(canonical(result) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print(f"FAIL:{error}")
        raise SystemExit(2)
