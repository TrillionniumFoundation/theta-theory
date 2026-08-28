#!/usr/bin/env python3
"""Coherent re-signed mutation attacks for the sealed T04 pair contract."""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


EXPECTED = {"CROSS_CHART_QUOTIENT_RECHART": 1_361_424,
            "SAME_CHART_TRANSVERSE_1D": 448,
            "CROSS_CHART_GRAPH_SIDE_T0": 192,
            "CODIMENSION_TWO_LOWER_OWNER": 24}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def result_contract(result: dict[str, Any]) -> None:
    pair = result["pair_contract"]
    need(result["status"].startswith("PASS_T04_DOUBLE_GRAPHS_1362088"), "status")
    need(pair["candidate_pairs"] == 1_362_088, "pair count")
    need(pair["bucket_census"] == EXPECTED, "bucket census")
    need(pair["bucket_sum"] == 1_362_088 == sum(pair["bucket_census"].values()), "bucket sum")
    need(pair["pair_owner_count_for_every_row"] == 1, "unique owner")
    need(pair["buckets_mutually_exclusive_by_typed_primitive_key"] is True, "mutual exclusion")
    need(pair["every_candidate_resolved"] is True and pair["unresolved"] == 0, "resolved")
    need(pair["legal_cross_component_same_physical_point_witnesses"] == 0, "zero witness")
    need(result["physical_witness_contract"]["witness_count"] == 0, "empty witness count")
    scope = result["scope"]
    for key in ("old_C27_FAMILIES_read_or_imported", "old_transition_ledger_read_or_imported",
                "C28_read_or_imported", "C29_read_or_imported",
                "historical_edge_ledger_used_as_candidate_universe"):
        need(scope[key] is False, "forbidden governance:" + key)
    need(result["P0A_graph_lower_cross_implementation"]
         ["projection_exact_across_two_semantic_implementations"] is True, "small dual impl")
    need(result["P0A_graph_lower_cross_implementation"]["coherent_attacks_rejected"] == 12,
         "inner attacks")
    need(result["formal_credit"] == 0 and result["manifest_authorized"] is False,
         "zero credit")


def row_contract(row: dict[str, Any]) -> None:
    body = dict(row); claim = body.pop("row_sha256", None)
    need(claim == digest(body), "row signature")
    need(row["bucket"] in EXPECTED, "known bucket")
    identity = {"T04_terminal": "DOUBLE_GRAPHS", "bucket": row["bucket"],
                "candidate_key": row["candidate_key"]}
    need(row["candidate_id"] == "t04-double-graphs-pair:" + digest(identity), "candidate id")
    need(row["candidate_key_sha256"] == digest(row["candidate_key"]), "candidate key")
    need(row["pair_owner_count"] == 1 and row["pair_owner_terminal"] == "T04_DOUBLE_GRAPHS",
         "pair owner")
    need(row["resolved"] is True and row["unresolved"] is False, "row resolved")
    need(row["legal_cross_component_same_physical_point_witness"] is False, "row witness")
    need(row["formal_credit"] == 0, "row credit")
    proof = row["exact_physical_proof"]
    if row["bucket"] == "CROSS_CHART_QUOTIENT_RECHART":
        need(proof["source_chart"] != proof["target_chart"], "cross chart")
        if proof["chart_relation"] == "OPPOSITE_DOMINANT_CHART":
            need(row["exact_disposition_route"]
                 == "EXACT_NONINCIDENCE__OPPOSITE_DOMINANT_STRICT_SIGN"
                 and Fraction(proof["target_radical_square_minimum_margin"]) > 0
                 and proof["normal_position_solution_set"] == "EMPTY", "opposite proof")
        else:
            need(proof["chart_relation"] == "PERPENDICULAR_DOMINANT_CHART"
                 and row["exact_disposition_route"]
                    == "EXACT_NONINCIDENCE__PERPENDICULAR_REQUIRES_EXCLUDED_UNIT_T_ENDPOINT"
                 and Fraction(proof["required_target_t"]) in {-1, 1}
                 and Fraction(proof["exact_gap_from_required_endpoint"]) > 0,
                 "perpendicular proof")
    elif row["bucket"] == "SAME_CHART_TRANSVERSE_1D":
        need(Fraction(proof["exact_p_gap"]) > 0
             and proof["same_point_solution_set"] == "EMPTY", "transverse proof")
    elif row["bucket"] == "CROSS_CHART_GRAPH_SIDE_T0":
        need(proof["source_chart"] != proof["target_chart"]
             and proof["source_position"] != proof["target_position"]
             and proof["same_point_solution_set"] == "EMPTY", "graph proof")
    else:
        need(proof["target_open_support_contains_contact"] is False
             and proof["complete_t0_owner_component_equals_source_component"] is True
             and proof["same_point_cross_component_witness"] is False,
             "lower proof")


def resign_row(row: dict[str, Any]) -> None:
    body = dict(row); body.pop("row_sha256", None)
    row["row_sha256"] = digest(body)


def rejected(function: Callable[[dict[str, Any]], None], value: dict[str, Any]) -> bool:
    try:
        function(value)
    except (Reject, KeyError, TypeError, ValueError):
        return True
    return False


def sample_rows(path: Path) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    with gzip.open(path, "rt", encoding="ascii") as stream:
        for line in stream:
            row = json.loads(line)
            found.setdefault(row["bucket"], row)
            if len(found) == 4:
                break
    need(set(found) == set(EXPECTED), "four bucket samples")
    for row in found.values(): row_contract(row)
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    candidate = Path(args.candidate)
    document = json.loads((candidate / "result.json").read_bytes())
    need(document["result_sha256"] == digest(document["result"]), "result wrapper")
    baseline = document["result"]
    result_contract(baseline)
    samples = sample_rows(candidate / "t04_double_graphs_1362088_pair_ownership.jsonl.gz")
    attacks: dict[str, bool] = {}

    result_mutations = {
        "pair_count_minus_one": lambda x: x["pair_contract"].__setitem__("candidate_pairs", 1_362_087),
        "pair_count_plus_one": lambda x: x["pair_contract"].__setitem__("candidate_pairs", 1_362_089),
        "cross_bucket_omit": lambda x: x["pair_contract"]["bucket_census"].__setitem__("CROSS_CHART_QUOTIENT_RECHART", 1_361_423),
        "transverse_bucket_duplicate": lambda x: x["pair_contract"]["bucket_census"].__setitem__("SAME_CHART_TRANSVERSE_1D", 449),
        "graph_bucket_omit": lambda x: x["pair_contract"]["bucket_census"].__setitem__("CROSS_CHART_GRAPH_SIDE_T0", 191),
        "lower_bucket_duplicate": lambda x: x["pair_contract"]["bucket_census"].__setitem__("CODIMENSION_TWO_LOWER_OWNER", 25),
        "bucket_sum_mutation": lambda x: x["pair_contract"].__setitem__("bucket_sum", 1_362_087),
        "owner_count_two": lambda x: x["pair_contract"].__setitem__("pair_owner_count_for_every_row", 2),
        "mutual_exclusion_false": lambda x: x["pair_contract"].__setitem__("buckets_mutually_exclusive_by_typed_primitive_key", False),
        "unresolved_one": lambda x: x["pair_contract"].__setitem__("unresolved", 1),
        "resolved_false": lambda x: x["pair_contract"].__setitem__("every_candidate_resolved", False),
        "witness_one": lambda x: x["pair_contract"].__setitem__("legal_cross_component_same_physical_point_witnesses", 1),
        "physical_witness_one": lambda x: x["physical_witness_contract"].__setitem__("witness_count", 1),
        "old_families_true": lambda x: x["scope"].__setitem__("old_C27_FAMILIES_read_or_imported", True),
        "old_transition_true": lambda x: x["scope"].__setitem__("old_transition_ledger_read_or_imported", True),
        "edge_universe_true": lambda x: x["scope"].__setitem__("historical_edge_ledger_used_as_candidate_universe", True),
        "small_dual_false": lambda x: x["P0A_graph_lower_cross_implementation"].__setitem__("projection_exact_across_two_semantic_implementations", False),
        "inner_attack_count_11": lambda x: x["P0A_graph_lower_cross_implementation"].__setitem__("coherent_attacks_rejected", 11),
        "formal_credit_one": lambda x: x.__setitem__("formal_credit", 1),
        "manifest_authorized_true": lambda x: x.__setitem__("manifest_authorized", True),
    }
    for name, mutate in result_mutations.items():
        item = copy.deepcopy(baseline); mutate(item)
        attacks[name] = rejected(result_contract, item)

    def row_attack(name: str, bucket: str, mutate: Callable[[dict[str, Any]], None]) -> None:
        item = copy.deepcopy(samples[bucket]); mutate(item); resign_row(item)
        attacks[name] = rejected(row_contract, item)

    row_attack("row_bucket_flip", "CROSS_CHART_QUOTIENT_RECHART",
               lambda x: x.__setitem__("bucket", "SAME_CHART_TRANSVERSE_1D"))
    row_attack("row_key_mutation", "CROSS_CHART_QUOTIENT_RECHART",
               lambda x: x["candidate_key"].__setitem__("R291_physical_witness_cell_index", 999999))
    row_attack("row_owner_two", "CROSS_CHART_QUOTIENT_RECHART",
               lambda x: x.__setitem__("pair_owner_count", 2))
    row_attack("row_unresolved", "CROSS_CHART_QUOTIENT_RECHART",
               lambda x: x.__setitem__("unresolved", True))
    row_attack("row_witness_flip", "CROSS_CHART_QUOTIENT_RECHART",
               lambda x: x.__setitem__("legal_cross_component_same_physical_point_witness", True))
    row_attack("opposite_margin_zero", "CROSS_CHART_QUOTIENT_RECHART",
               lambda x: x["exact_physical_proof"].__setitem__("target_radical_square_minimum_margin", "0"))
    row_attack("transverse_gap_zero", "SAME_CHART_TRANSVERSE_1D",
               lambda x: x["exact_physical_proof"].__setitem__("exact_p_gap", "0"))
    row_attack("graph_position_equal", "CROSS_CHART_GRAPH_SIDE_T0",
               lambda x: x["exact_physical_proof"].__setitem__("target_position", x["exact_physical_proof"]["source_position"]))
    row_attack("lower_open_contains_true", "CODIMENSION_TWO_LOWER_OWNER",
               lambda x: x["exact_physical_proof"].__setitem__("target_open_support_contains_contact", True))
    row_attack("lower_owner_component_false", "CODIMENSION_TWO_LOWER_OWNER",
               lambda x: x["exact_physical_proof"].__setitem__("complete_t0_owner_component_equals_source_component", False))
    row_attack("lower_witness_true", "CODIMENSION_TWO_LOWER_OWNER",
               lambda x: x["exact_physical_proof"].__setitem__("same_point_cross_component_witness", True))

    need(len(attacks) == 31 and all(attacks.values()), "31 coherent mutations rejected")
    body = {
        "schema": "cm2.c27-independent.t04-double-graphs.pair-ownership-coherent-attacks.v1",
        "status": "PASS_31_OF_31_COHERENT_RESIGNED_ATTACKS_REJECTED",
        "attack_count": 31, "accepted": 0, "rejected": 31,
        "attacks": attacks, "formal_credit": 0, "manifest_authorized": False,
    }
    wrapper = {**body, "attack_receipt_sha256": digest(body)}
    output = Path(args.output); need(not output.exists(), "fresh attack receipt")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encode(wrapper) + b"\n")
    print(encode(wrapper).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print("T04_ATTACK_REJECT:" + str(exc))
        raise SystemExit(2)
