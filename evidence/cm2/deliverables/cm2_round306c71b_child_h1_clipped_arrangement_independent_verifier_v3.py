#!/usr/bin/env python3
"""No-producer verifier for the C71b v3 exact clipped H1 arrangement.

The verifier does not import, open, read, decode, compile, or execute the C71b
producer.  It independently derives each expected v3 row from the frozen,
no-producer-verified C71 v2 ledger and compares the complete canonical object.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import itertools
import json
import os
import re
import stat
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterator

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
SELF = Path(__file__).resolve()
PREFIX = "cm2_round306c71b_child_h1_clipped_arrangement_successor_v3"
SCHEMA = "cm2.round306c71b.child-h1-clipped-arrangement-successor.v3"
CONTRACT_NAME = "cm2_round306c71b_child_h1_clipped_arrangement_contract_v3.json"
SCHEMAS_NAME = "cm2_round306c71b_child_h1_clipped_arrangement_closed_schemas_v3.json"
ROWS_NAME = PREFIX + "_rows.jsonl.gz"
RESULT_NAME = PREFIX + "_result.json"

CONTRACT_FILE_SHA256 = "38942f45e5a357aa6f730587b2d160469c7f20344e6daa333a891484b4a1ecbf"
CONTRACT_OBJECT_SHA256 = "c25ce17c9485c61cdba417cd014824ef24f28632d1490d867e355c052c306dbb"
SCHEMAS_FILE_SHA256 = "e8e43e6c2fc4b842d2def2b51e6b7323542c3ef0bd3424069618bc6e07f4bafa"
SCHEMAS_OBJECT_SHA256 = "e8cf6939456387210e3380fd5bbea2af6683fe1835d9e5ea577739e884511a75"

V2_NAMES = {
    "rows": "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_v2_intersection_rows.jsonl.gz",
    "summaries": "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_v2_source_summaries.jsonl.gz",
    "result": "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_v2_result.json",
    "report": "cm2_round306c71_c65v9_c69c_c70_child_h1_successor_v2_report.md",
    "verification": "independent_verification_v2.json",
}
EXPECTED_CENSUS = {
    "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE": 134155,
    "LOCAL_H1_STRICT_NEGATIVE_FULL_CHILD_BOX": 1,
    "LOCAL_H1_STRICT_POSITIVE_FULL_CHILD_BOX": 7352,
    "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS": 8093,
    "PROVED_CHILD_H1_ZERO_CONTACT__BOUNDARY_ARRANGEMENT_UNSEALED": 17654,
}
EXPECTED_TOTAL = 167255
EXPECTED_NUMERIC = 33100
EXPECTED_CLIPPED = 17654
EDGE_ORDER = ("T_LOW", "T_HIGH", "P_LOW", "P_HIGH")
ZERO = {"terminal_disposition_credit": 0, "formal_credit": 0,
        "whole_parent_credit": 0, "D02_gate_credit": 0}


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in out, "duplicate JSON key:" + key)
        out[key] = value
    return out


def reject_float(token: str) -> Any:
    raise Reject("JSON float forbidden:" + token)


def parse_json(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw, object_pairs_hook=no_duplicates,
                           parse_float=reject_float, parse_constant=reject_float)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Reject(label + ": invalid JSON") from exc
    need(isinstance(value, dict), label + ": JSON object")
    return value


def close_object(value: dict[str, Any], expected: str | None, label: str) -> None:
    claim = value.get("object_sha256")
    need(isinstance(claim, str), label + ": object hash")
    body = dict(value)
    del body["object_sha256"]
    need(digest(body) == claim and (expected is None or claim == expected),
         label + ": object closure")


def close_row(row: dict[str, Any], label: str) -> None:
    claim = row.get("row_sha256")
    need(isinstance(claim, str), label + ": row hash")
    body = dict(row)
    del body["row_sha256"]
    need(digest(body) == claim, label + ": row closure")


def secure_bytes(path: Path, expected: str, label: str) -> bytes:
    need(path.is_absolute() and path.exists() and not path.is_symlink(),
         label + ": regular path")
    before = path.stat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
         label + ": regular single link")
    raw = path.read_bytes()
    after = path.stat()
    need((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns,
          before.st_ctime_ns) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns,
          after.st_ctime_ns), label + ": stable read")
    need(hashlib.sha256(raw).hexdigest() == expected, label + ": file pin")
    return raw


def load_gate(v2_stage: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    need("__PIN_" not in CONTRACT_FILE_SHA256, "contract pin not frozen")
    contract = parse_json(secure_bytes(HERE / CONTRACT_NAME,
                                       CONTRACT_FILE_SHA256, "contract"), "contract")
    schemas = parse_json(secure_bytes(HERE / SCHEMAS_NAME,
                                      SCHEMAS_FILE_SHA256, "schemas"), "schemas")
    close_object(contract, CONTRACT_OBJECT_SHA256, "contract")
    close_object(schemas, SCHEMAS_OBJECT_SHA256, "schemas")
    need(contract["closed_schemas"]["object_sha256"] == SCHEMAS_OBJECT_SHA256,
         "contract/schema binding")
    pins = contract["frozen_C71_v2_stage"]
    for key, filename in V2_NAMES.items():
        secure_bytes(v2_stage / filename, pins[key], "v2 " + key)
    result = parse_json((v2_stage / V2_NAMES["result"]).read_bytes(), "v2 result")
    verification = parse_json((v2_stage / V2_NAMES["verification"]).read_bytes(),
                              "v2 verification")
    close_object(result, pins["result_object_sha256"], "v2 result")
    close_object(verification, pins["verification_object_sha256"], "v2 verification")
    v2_attacks = verification["coherent_attacks"]
    need(verification["status"].startswith("PASS_NO_PRODUCER_EXACT_REBUILD") and
         verification["producer_source_imported_read_decoded_compiled_or_executed"] is False and
         v2_attacks["attack_count"] == 20 and
         v2_attacks["status"] ==
            "PASS_20_OF_20_COHERENT_CHILD_AND_CREDIT_ATTACKS_FAIL_CLOSED" and
         len(v2_attacks["attacks"]) == 20 and
         all(value == "FAIL_CLOSED" for value in v2_attacks["attacks"].values()),
         "v2 no-producer verification and 20/20 attack gate")
    need(result["coverage"]["numeric_disposition_census"] == EXPECTED_CENSUS,
         "v2 census")
    return contract, result


def iter_rows(path: Path, label: str) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, raw in enumerate(stream):
            need(raw.endswith(b"\n"), label + ": newline")
            row = parse_json(raw, label + " " + str(ordinal))
            close_row(row, label + " " + str(ordinal))
            yield row


def strict_sign(payload: dict[str, Any], label: str) -> int:
    need(payload.get("contains_zero") is False, label + ": strict")
    signs: list[int] = []
    for key in ("lower", "upper"):
        match = re.match(r"^\[?([+-]?)((?:\d)|(?:\.\d))", payload[key].strip())
        need(match is not None, label + ": printable bound")
        signs.append(-1 if match.group(1) == "-" else 1)
    need(signs[0] == signs[1], label + ": bound sign agreement")
    return signs[0]


def q(text: str) -> Fraction:
    try:
        return Fraction(text)
    except (ValueError, ZeroDivisionError) as exc:
        raise Reject("invalid rational coordinate") from exc


def sign_name(sign: int) -> str:
    need(sign in (-1, 1), "strict sign")
    return "NEGATIVE" if sign < 0 else "POSITIVE"


def independent_specs(box: dict[str, list[str]]) -> dict[str, dict[str, Any]]:
    t0, t1 = box["t"]
    p0, p1 = box["p"]
    need(q(t0) < q(t1) and q(p0) < q(p1) and box["s"] == ["0", "0"],
         "exact 2D child")
    return {
        "T_LOW": {"fixed_axis": "t", "fixed_value": t0,
                  "varying_axis": "p", "varying_interval": [p0, p1],
                  "ends": [(t0, p0), (t0, p1)]},
        "T_HIGH": {"fixed_axis": "t", "fixed_value": t1,
                   "varying_axis": "p", "varying_interval": [p0, p1],
                   "ends": [(t1, p0), (t1, p1)]},
        "P_LOW": {"fixed_axis": "p", "fixed_value": p0,
                  "varying_axis": "t", "varying_interval": [t0, t1],
                  "ends": [(t0, p0), (t1, p0)]},
        "P_HIGH": {"fixed_axis": "p", "fixed_value": p1,
                   "varying_axis": "t", "varying_interval": [t0, t1],
                   "ends": [(t0, p1), (t1, p1)]},
    }


def independent_corners(v2: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    rows = v2["H1_child_certificate"]["strict_corner_records"]
    need(len(rows) == 4, "four corners")
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        need(row["sign"] in (-1, 1) and row["H1"]["contains_zero"] is False and
             row["point"]["s"] == "0", "strict corner")
        key = (row["point"]["t"], row["point"]["p"])
        need(key not in out, "distinct corner")
        out[key] = row
    return out


def independent_projection_coordinate(spec: dict[str, Any], root: str) -> dict[str, Any]:
    if spec["fixed_axis"] == "p":
        return {"kind": "EXACT_RATIONAL", "value": spec["fixed_value"]}
    return {"kind": "UNIQUE_EDGE_ROOT_COORDINATE", "axis": "p",
            "root_id": root,
            "exact_isolating_open_interval": spec["varying_interval"]}


def independent_projection_order(crossings: list[str], slope: int) -> tuple[str, str, str]:
    if "P_LOW" in crossings:
        other = next(edge for edge in crossings if edge != "P_LOW")
        return "R_P_LOW", "R_" + other, "P_LOW_IS_EXACT_PROJECTION_MINIMUM"
    if "P_HIGH" in crossings:
        other = next(edge for edge in crossings if edge != "P_HIGH")
        return "R_" + other, "R_P_HIGH", "P_HIGH_IS_EXACT_PROJECTION_MAXIMUM"
    need(set(crossings) == {"T_LOW", "T_HIGH"}, "projection crossing pair")
    if slope > 0:
        return "R_T_LOW", "R_T_HIGH", "STRICT_POSITIVE_IMPLICIT_GRAPH_SLOPE"
    return "R_T_HIGH", "R_T_LOW", "STRICT_NEGATIVE_IMPLICIT_GRAPH_SLOPE"


def independent_closure(v2: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    cert = v2["H1_child_certificate"]
    deriv = cert["full_child_box_derivatives"]
    dt, dp = strict_sign(deriv["t"], "dt"), strict_sign(deriv["p"], "dp")
    need(deriv["s"]["contains_zero"] is True, "s constant")
    corners = independent_corners(v2)
    specs = independent_specs(v2["exact_representative_box"])
    edges: list[dict[str, Any]] = []
    roots: list[dict[str, Any]] = []
    crossings: list[str] = []
    for edge_id in EDGE_ORDER:
        spec = specs[edge_id]
        a, b = (corners[spec["ends"][0]], corners[spec["ends"][1]])
        signs = [a["sign"], b["sign"]]
        tangent_sign = dt if spec["varying_axis"] == "t" else dp
        need((tangent_sign > 0 and signs[0] <= signs[1]) or
             (tangent_sign < 0 and signs[0] >= signs[1]),
             "strict monotone edge order")
        common = {"edge_id": edge_id, "fixed_axis": spec["fixed_axis"],
                  "fixed_value": spec["fixed_value"],
                  "varying_axis": spec["varying_axis"],
                  "exact_closed_interval": spec["varying_interval"],
                  "ordered_endpoint_signs": signs,
                  "ordered_endpoint_H1_intervals": [a["H1"], b["H1"]],
                  "strict_tangential_derivative_bounds": deriv[spec["varying_axis"]],
                  "strict_tangential_derivative_sign": sign_name(tangent_sign)}
        if signs[0] != signs[1]:
            crossings.append(edge_id)
            rid = "R_" + edge_id
            roots.append({"root_id": rid, "edge_id": edge_id,
                          "definition": "THE_UNIQUE_H1_ZERO_ON_THE_OPEN_EDGE",
                          "fixed_axis": spec["fixed_axis"],
                          "fixed_value": spec["fixed_value"],
                          "varying_axis": spec["varying_axis"],
                          "exact_isolating_open_interval": spec["varying_interval"],
                          "strict_opposite_endpoint_signs": signs,
                          "existence_by_IVT": True,
                          "uniqueness_by_uniform_strict_tangential_derivative": True,
                          "not_a_corner": True,
                          "projection_coordinate":
                              independent_projection_coordinate(spec, rid)})
            edges.append({**common, "edge_disposition": "ONE_UNIQUE_INTERIOR_H1_ZERO",
                          "root_id": rid})
        else:
            edges.append({**common,
                          "edge_disposition": "STRICT_NO_ZERO_" + sign_name(signs[0]),
                          "strict_whole_edge_sign": sign_name(signs[0]),
                          "root_id": None})
    need(len(crossings) == len(roots) == 2, "two exact boundary roots")
    slope = -dt * dp
    lo, hi, why = independent_projection_order(crossings, slope)
    root_map = {root["root_id"]: root for root in roots}
    partition = {
        "H1_LT_0": "EXACT_OPEN_NEGATIVE_REGION_CUT_BY_CLIPPED_GRAPH",
        "H1_EQ_0": "EXACT_SINGLE_CLIPPED_REGULAR_GRAPH_ARC",
        "H1_GT_0": "EXACT_OPEN_POSITIVE_REGION_CUT_BY_CLIPPED_GRAPH",
        "pairwise_disjoint": True, "union_exact_child": True,
        "zero_carrier_has_exactly_two_boundary_endpoints": True,
        "zero_carrier_has_no_corner_incidence": True,
        "graph_full_dimensional_Kraft_weight": "0",
        "half_open_negative_owner": {"predicate": "H1<=0", "owns_graph": True},
        "half_open_positive_owner": {"predicate": "H1>0", "owns_graph": False},
    }
    closure = {
        "kind": "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFF_GRAPH_REGIONS",
        "precision_bits": 384, "equation": "H1=n1_x^2-n1_y^2",
        "v2_child_certificate_sha256": digest(cert),
        "full_child_strict_derivatives": {
            "t": {"sign": sign_name(dt), "bounds": deriv["t"]},
            "p": {"sign": sign_name(dp), "bounds": deriv["p"]}},
        "four_strict_nonzero_corners": sorted(cert["strict_corner_records"],
                                               key=lambda x: (q(x["point"]["t"]),
                                                              q(x["point"]["p"]))),
        "corner_zero_incidence_count": 0,
        "boundary_edges": edges, "boundary_root_count": 2,
        "boundary_roots": roots, "boundary_crossing_edge_ids": crossings,
        "clipped_graph": {
            "dependent_axis": "t", "projection_axis": "p",
            "uniform_nonzero_dependent_derivative": True,
            "implicit_graph_derivative_sign": sign_name(slope),
            "exact_projection_domain": {
                "kind": "EXACT_CLOSED_INTERVAL_BETWEEN_UNIQUE_BOUNDARY_ROOT_PROJECTIONS",
                "lower_endpoint": root_map[lo]["projection_coordinate"],
                "lower_root_id": lo,
                "upper_endpoint": root_map[hi]["projection_coordinate"],
                "upper_root_id": hi, "strict_order_proof": why},
            "fiber_zero_count_on_projection_domain": "EXACTLY_ONE",
            "fiber_zero_count_outside_projection_domain": "ZERO",
            "below_graph_H1_sign": sign_name(-dt),
            "above_graph_H1_sign": sign_name(dt),
            "lower_projection_exterior_H1_sign": sign_name(-dp),
            "upper_projection_exterior_H1_sign": sign_name(dp),
            "single_connected_arc": True,
            "no_closed_or_disconnected_zero_component": True},
        "closure_theorem": {
            "boundary_exhaustive": True, "projection_coverage": True,
            "fiber_uniqueness": True, "two_sides_strict": True,
            "coverage_and_mutual_exclusion": True,
            "reason": "STRICT_DT_GIVES_AT_MOST_ONE_ZERO_PER_P_FIBER;_STRICT_DP_MAKES_BOTH_T_BOUNDARY_TRACES_STRICT;_FOUR_EDGE_CENSUS_GIVES_ONE_EXACT_PROJECTION_INTERVAL_AND_TWO_ENDPOINTS"},
    }
    return closure, partition


def independent_expected(v2: dict[str, Any]) -> dict[str, Any]:
    for key, value in ZERO.items():
        need(v2[key] == value, "v2 row credit")
    need(v2["global_consumption_ready"] is False, "v2 row global boundary")
    old = v2["intersection_disposition"]
    base = {
        "schema": SCHEMA + ".arrangement-row",
        "v2_intersection_row_sha256": v2["row_sha256"],
        "C65_aggregate_leaf_row_sha256": v2["C65_aggregate_leaf_row_sha256"],
        "source_C61_aggregate_leaf_row_sha256": v2["source_C61_aggregate_leaf_row_sha256"],
        "pair_index": v2["pair_index"], "source_path": v2["source_path"],
        "child_path": v2["child_path"],
        "exact_representative_box": v2["exact_representative_box"],
        "v2_disposition": old, "global_consumption_ready": False, **ZERO}
    if old == "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE":
        return {**base, "child_numeric_domain": False,
                "arrangement_disposition": old, "H1_full_box_closure": None,
                "three_strata_partition": None,
                "child_level_H1_full_box_closed": False,
                "consumer_review_ready": False,
                "remaining_blocker_codes": v2["remaining_blocker_codes"]}
    if old == "PROVED_CHILD_H1_ZERO_CONTACT__BOUNDARY_ARRANGEMENT_UNSEALED":
        closure, partition = independent_closure(v2)
        new = "LOCAL_H1_CLIPPED_GRAPH_AND_TWO_OFF_GRAPH_REGIONS"
    else:
        need(old in EXPECTED_CENSUS and v2["consumer_review_ready"] is True and
             v2["three_strata_partition"]["pairwise_disjoint"] is True and
             v2["three_strata_partition"]["union_exact_child"] is True,
             "existing v2 closure")
        closure = {"kind": "INDEPENDENTLY_VERIFIED_C71_V2_FULL_BOX_CLOSURE_REPLAY",
                   "v2_method": v2["H1_child_certificate"]["accepted_full_box_method"],
                   "v2_child_certificate_sha256": digest(v2["H1_child_certificate"]),
                   "v2_three_strata_partition_sha256": digest(v2["three_strata_partition"])}
        partition, new = v2["three_strata_partition"], old
    return {**base, "child_numeric_domain": True,
            "arrangement_disposition": new, "H1_full_box_closure": closure,
            "three_strata_partition": partition,
            "child_level_H1_full_box_closed": True,
            "consumer_review_ready": True, "remaining_blocker_codes": []}


def exact_guard(v2: dict[str, Any], observed: dict[str, Any], label: str) -> None:
    close_row(observed, label)
    body = dict(observed)
    del body["row_sha256"]
    need(body == independent_expected(v2), label + ": exact independent rebuild")


def mutate(body: dict[str, Any], kind: str) -> dict[str, Any]:
    value = copy.deepcopy(body)
    value.pop("row_sha256", None)
    if kind == "credit":
        value["formal_credit"] = 1
    elif kind == "global":
        value["global_consumption_ready"] = True
    elif kind == "child_path":
        value["child_path"] += "0"
    elif kind == "v2_pin":
        value["v2_intersection_row_sha256"] = "0" * 64
    elif kind == "ready":
        value["consumer_review_ready"] = not value["consumer_review_ready"]
    elif kind == "disposition":
        value["arrangement_disposition"] += "_MUTATED"
    elif kind == "root_count":
        value["H1_full_box_closure"]["boundary_root_count"] = 1
    elif kind == "projection_axis":
        value["H1_full_box_closure"]["clipped_graph"]["projection_axis"] = "t"
    elif kind == "coverage":
        value["three_strata_partition"]["union_exact_child"] = False
    elif kind == "edge_root":
        value["H1_full_box_closure"]["boundary_edges"][0]["root_id"] = "R_FAKE"
    else:
        raise Reject("unknown attack")
    return {**value, "row_sha256": digest(value)}


def coherent_attacks(samples: dict[str, tuple[dict[str, Any], dict[str, Any]]]) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    generic = ("credit", "global", "child_path", "v2_pin", "ready", "disposition")
    for sample_name, (v2, observed) in samples.items():
        for kind in generic:
            rejected = False
            try:
                exact_guard(v2, mutate(observed, kind), "attack")
            except Reject:
                rejected = True
            attempts.append({"sample": sample_name, "mutation": kind,
                             "hash_reclosed": True, "rejected": rejected})
    v2, observed = samples["clipped"]
    for kind in ("root_count", "projection_axis", "coverage", "edge_root"):
        rejected = False
        try:
            exact_guard(v2, mutate(observed, kind), "clipped attack")
        except Reject:
            rejected = True
        attempts.append({"sample": "clipped", "mutation": kind,
                         "hash_reclosed": True, "rejected": rejected})
    need(len(attempts) >= 20 and all(row["rejected"] for row in attempts),
         "coherent attack suite")
    return {"attempted": len(attempts), "rejected": len(attempts),
            "all_hash_reclosed_before_attack": True,
            "all_rejected": True, "attempts": attempts}


def exclusive_write(path: Path, raw: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                         getattr(os, "O_NOFOLLOW", 0), 0o444)
    try:
        view = memoryview(raw)
        while view:
            wrote = os.write(descriptor, view)
            need(wrote > 0, "write progress")
            view = view[wrote:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    need(path.read_bytes() == raw and path.stat().st_nlink == 1,
         "verification terminal-byte replay")


def verify(v2_stage: Path, candidate: Path, output: Path) -> dict[str, Any]:
    contract, v2_result = load_gate(v2_stage.resolve())
    need(candidate.is_absolute() and candidate.is_dir() and not candidate.is_symlink(),
         "candidate directory")
    result = parse_json((candidate / RESULT_NAME).read_bytes(), "candidate result")
    close_object(result, None, "candidate result")
    descriptor = result["ledgers"]["arrangement_rows"]
    rows_path = candidate / ROWS_NAME
    need(file_sha(rows_path) == descriptor["sha256"] and
         rows_path.stat().st_size == descriptor["size"] and
         descriptor["row_count"] == EXPECTED_TOTAL,
         "candidate ledger descriptor")
    counts: Counter[str] = Counter()
    sequence = hashlib.sha256()
    samples: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    v2_iter = iter_rows(v2_stage / V2_NAMES["rows"], "v2 row")
    candidate_iter = iter_rows(rows_path, "candidate row")
    count = 0
    for pair in itertools.zip_longest(v2_iter, candidate_iter):
        need(pair[0] is not None and pair[1] is not None, "same ledger length")
        v2, observed = pair
        exact_guard(v2, observed, "candidate exact row " + str(count))
        counts[v2["intersection_disposition"]] += 1
        sequence.update((observed["row_sha256"] + "\n").encode("ascii"))
        old = v2["intersection_disposition"]
        if old == "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE":
            samples.setdefault("blocked", (v2, observed))
        elif old.startswith("LOCAL_H1_STRICT_"):
            samples.setdefault("strict", (v2, observed))
        elif old == "LOCAL_H1_UNIQUE_GRAPH_AND_TWO_OFF_GRAPH_SLABS":
            samples.setdefault("full_graph", (v2, observed))
        elif old == "PROVED_CHILD_H1_ZERO_CONTACT__BOUNDARY_ARRANGEMENT_UNSEALED":
            samples.setdefault("clipped", (v2, observed))
        count += 1
    need(count == EXPECTED_TOTAL and dict(counts) == EXPECTED_CENSUS,
         "complete independent census")
    need(sequence.hexdigest() == descriptor["row_hash_line_sequence_sha256"],
         "row sequence descriptor")
    need(set(samples) == {"blocked", "strict", "full_graph", "clipped"},
         "attack samples")
    need(result["coverage"]["child_level_H1_full_box_closed_count"] == EXPECTED_NUMERIC and
         result["coverage"]["new_exact_clipped_arrangement_child_count"] == EXPECTED_CLIPPED,
         "result numeric closure")
    need(result["proof_invariants"]["all_33100_numeric_children_have_full_box_H1_closure"] is True and
         result["proof_invariants"]["all_134155_nondecision_children_remain_fail_closed"] is True,
         "result proof invariants")
    for key, value in ZERO.items():
        need(result[key] == value, "candidate zero credit:" + key)
    need(result["candidate_is_authority"] is False and
         result["global_consumption_ready"] is False and
         result["runtime_canonical_pointer_or_seal_writes"] is False,
         "candidate authority boundary")
    attacks = coherent_attacks(samples)
    verification = {
        "schema": SCHEMA + ".independent-verification.v3",
        "status": "PASS_NO_PRODUCER_EXACT_REBUILD__33100_CHILD_H1_FULL_BOX_CLOSED__17654_EXACT_CLIPPED_ARRANGEMENTS__28_COHERENT_ATTACKS__ZERO_CREDIT",
        "verifier_file_sha256": file_sha(SELF),
        "candidate_result_object_sha256": result["object_sha256"],
        "candidate_producer_file_sha256_claim_treated_as_opaque":
            result["producer_file_sha256"],
        "producer_source_imported_read_decoded_compiled_or_executed": False,
        "old_C71_skeleton_imported_read_decoded_compiled_or_executed": False,
        "frozen_inputs": {
            "contract_object_sha256": CONTRACT_OBJECT_SHA256,
            "schemas_object_sha256": SCHEMAS_OBJECT_SHA256,
            "C71_v2_result_object_sha256": v2_result["object_sha256"],
            "C71_v2_independent_verification_object_sha256":
                contract["frozen_C71_v2_stage"]["verification_object_sha256"]},
        "coverage": {"arrangement_row_count": count,
                     "decision_source_child_count": EXPECTED_NUMERIC,
                     "blocker_source_child_count": EXPECTED_TOTAL - EXPECTED_NUMERIC,
                     "new_exact_clipped_arrangement_child_count": EXPECTED_CLIPPED,
                     "child_level_H1_full_box_closed_count": EXPECTED_NUMERIC,
                     "v2_disposition_census": dict(sorted(counts.items()))},
        "actual_descriptor": {"filename": ROWS_NAME,
                              "sha256": file_sha(rows_path),
                              "size": rows_path.stat().st_size,
                              "row_count": count,
                              "row_hash_line_sequence_sha256": sequence.hexdigest()},
        "coherent_attacks": attacks,
        "candidate_is_authority": False, "global_consumption_ready": False,
        "runtime_canonical_pointer_or_seal_writes": False, **ZERO,
    }
    verification["object_sha256"] = digest(verification)
    exclusive_write(output.resolve(), canonical(verification) + b"\n")
    return verification


def static_self_test() -> dict[str, Any]:
    tests: dict[str, bool] = {}
    try:
        parse_json(b'{"a":1,"a":2}\n', "duplicate")
    except Reject:
        tests["duplicate_json_rejected"] = True
    tests.update({
        "partition_exact": EXPECTED_NUMERIC + 134155 == EXPECTED_TOTAL,
        "clipped_exact": EXPECTED_CLIPPED == 17654,
        "credit_lock": all(value == 0 for value in ZERO.values()),
        "no_producer_import": all("successor_v3" not in name for name in sys.modules),
        "old_skeleton_not_dependency": "skeleton_v1" not in " ".join(V2_NAMES.values()),
        "four_edges": len(EDGE_ORDER) == len(set(EDGE_ORDER)) == 4,
    })
    need(all(tests.values()), "static self-test")
    return {"schema": SCHEMA + ".independent-verifier-static-self-test.v3",
            "status": "PASS_7_OF_7_NO_PRODUCER_PARTITION_EDGE_JSON_AND_CREDIT_TESTS",
            "tests": tests, "files_written": False,
            "global_consumption_ready": False, **ZERO}


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--verify", type=Path)
    parser.add_argument("--v2-stage", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.self_test:
            need(args.v2_stage is None and args.output is None, "self-test writes nothing")
            result = static_self_test()
        else:
            need(args.v2_stage is not None and args.output is not None and
                 not args.output.exists() and not args.output.is_symlink(),
                 "fresh verification output and v2 stage")
            result = verify(args.v2_stage, args.verify.resolve(), args.output)
        print(canonical(result).decode("ascii"))
        return 0
    except (Reject, KeyError, TypeError, ValueError, OSError) as exc:
        print(canonical({"status": "REJECTED", "reason": str(exc)}).decode("ascii"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
