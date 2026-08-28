#!/usr/bin/env python3
"""C71b v3: close the exact H1 boundary arrangement left open by C71 v2.

This is a zero-credit successor.  It consumes only the frozen, independently
verified C71 v2 stage.  For each mixed-sign v2 child it turns the two strict
coordinate derivatives and four strict corners into four exact edge records,
two uniquely-defined boundary roots, one clipped regular graph, and its two
off-graph open regions.  It never runs or imports the rejected C71 skeleton.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
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
REPORT_NAME = PREFIX + "_report.md"

# Patched only after the v2 no-producer verifier has published its immutable
# result.  A placeholder makes accidental premature execution fail closed.
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


def close_object(value: dict[str, Any], expected: str, label: str) -> None:
    claim = value.get("object_sha256")
    need(isinstance(claim, str), label + ": object hash")
    body = dict(value)
    del body["object_sha256"]
    need(digest(body) == claim == expected, label + ": object closure")


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
    v2_result = parse_json((v2_stage / V2_NAMES["result"]).read_bytes(), "v2 result")
    close_object(v2_result, pins["result_object_sha256"], "v2 result")
    verification = parse_json((v2_stage / V2_NAMES["verification"]).read_bytes(),
                              "v2 verification")
    close_object(verification, pins["verification_object_sha256"], "v2 verification")
    need(verification["status"].startswith("PASS_NO_PRODUCER_EXACT_REBUILD"),
         "v2 independent verification status")
    need(verification["producer_source_imported_read_decoded_compiled_or_executed"] is False,
         "v2 verifier no-producer boundary")
    need(verification["coverage"]["intersection_row_count"] == EXPECTED_TOTAL and
         verification["coverage"]["decision_source_child_count"] == EXPECTED_NUMERIC,
         "v2 verified coverage")
    v2_attacks = verification["coherent_attacks"]
    need(v2_attacks["attack_count"] == 20 and
         v2_attacks["status"] ==
            "PASS_20_OF_20_COHERENT_CHILD_AND_CREDIT_ATTACKS_FAIL_CLOSED" and
         len(v2_attacks["attacks"]) == 20 and
         all(value == "FAIL_CLOSED" for value in v2_attacks["attacks"].values()),
         "v2 20/20 coherent attacks fail closed")
    for key, value in ZERO.items():
        need(v2_result[key] == value and verification[key] == value,
             "v2 zero credit:" + key)
    need(v2_result["global_consumption_ready"] is False and
         verification["global_consumption_ready"] is False,
         "v2 global boundary")
    need(v2_result["coverage"]["numeric_disposition_census"] == EXPECTED_CENSUS,
         "v2 census")
    return contract, v2_result


def iter_gzip_rows(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rb") as stream:
        for ordinal, raw in enumerate(stream):
            need(raw.endswith(b"\n"), "v2 row newline")
            row = parse_json(raw, "v2 row " + str(ordinal))
            close_row(row, "v2 row " + str(ordinal))
            yield row


def strict_payload_sign(payload: dict[str, Any], label: str) -> int:
    need(payload.get("contains_zero") is False, label + ": strict interval")
    signs: list[int] = []
    for key in ("lower", "upper"):
        text = payload[key].strip()
        match = re.match(r"^\[?([+-]?)((?:\d)|(?:\.\d))", text)
        need(match is not None, label + ": printable strict bound")
        signs.append(-1 if match.group(1) == "-" else 1)
    need(signs[0] == signs[1], label + ": bound signs agree")
    return signs[0]


def fraction_text(value: str) -> Fraction:
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise Reject("invalid rational coordinate") from exc


def corner_map(v2: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    rows = v2["H1_child_certificate"]["strict_corner_records"]
    need(len(rows) == 4, "four strict corners")
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        need(row["sign"] in (-1, 1) and row["H1"]["contains_zero"] is False,
             "strict corner")
        point = row["point"]
        need(point["s"] == "0", "C2 child lies on s=0")
        key = (point["t"], point["p"])
        need(key not in out, "unique corner")
        out[key] = row
    return out


def edge_specs(box: dict[str, list[str]]) -> dict[str, dict[str, Any]]:
    t0, t1 = box["t"]
    p0, p1 = box["p"]
    need(fraction_text(t0) < fraction_text(t1) and
         fraction_text(p0) < fraction_text(p1) and box["s"] == ["0", "0"],
         "positive 2D exact child")
    return {
        "T_LOW": {"fixed_axis": "t", "fixed_value": t0,
                  "varying_axis": "p", "varying_interval": [p0, p1],
                  "corners": [(t0, p0), (t0, p1)]},
        "T_HIGH": {"fixed_axis": "t", "fixed_value": t1,
                   "varying_axis": "p", "varying_interval": [p0, p1],
                   "corners": [(t1, p0), (t1, p1)]},
        "P_LOW": {"fixed_axis": "p", "fixed_value": p0,
                  "varying_axis": "t", "varying_interval": [t0, t1],
                  "corners": [(t0, p0), (t1, p0)]},
        "P_HIGH": {"fixed_axis": "p", "fixed_value": p1,
                   "varying_axis": "t", "varying_interval": [t0, t1],
                   "corners": [(t0, p1), (t1, p1)]},
    }


def sign_name(sign: int) -> str:
    need(sign in (-1, 1), "strict sign")
    return "NEGATIVE" if sign < 0 else "POSITIVE"


def projection_coordinate(edge_id: str, spec: dict[str, Any], root_id: str) -> dict[str, Any]:
    if spec["fixed_axis"] == "p":
        return {"kind": "EXACT_RATIONAL", "value": spec["fixed_value"]}
    return {"kind": "UNIQUE_EDGE_ROOT_COORDINATE", "axis": "p",
            "root_id": root_id,
            "exact_isolating_open_interval": spec["varying_interval"]}


def projection_order(crossings: list[str], specs: dict[str, dict[str, Any]],
                     slope_sign: int) -> tuple[str, str, str]:
    need(len(crossings) == 2, "two crossing edges")
    if "P_LOW" in crossings:
        other = crossings[0] if crossings[1] == "P_LOW" else crossings[1]
        return "R_P_LOW", "R_" + other, "P_LOW_IS_EXACT_PROJECTION_MINIMUM"
    if "P_HIGH" in crossings:
        other = crossings[0] if crossings[1] == "P_HIGH" else crossings[1]
        return "R_" + other, "R_P_HIGH", "P_HIGH_IS_EXACT_PROJECTION_MAXIMUM"
    need(set(crossings) == {"T_LOW", "T_HIGH"}, "supported crossing pair")
    if slope_sign > 0:
        return "R_T_LOW", "R_T_HIGH", "STRICT_POSITIVE_IMPLICIT_GRAPH_SLOPE"
    return "R_T_HIGH", "R_T_LOW", "STRICT_NEGATIVE_IMPLICIT_GRAPH_SLOPE"


def clipped_certificate(v2: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    cert = v2["H1_child_certificate"]
    derivatives = cert["full_child_box_derivatives"]
    dt = strict_payload_sign(derivatives["t"], "dH1/dt")
    dp = strict_payload_sign(derivatives["p"], "dH1/dp")
    need(derivatives["s"]["contains_zero"] is True, "constant s derivative")
    corners = corner_map(v2)
    specs = edge_specs(v2["exact_representative_box"])
    edge_rows: list[dict[str, Any]] = []
    roots: list[dict[str, Any]] = []
    crossings: list[str] = []
    for edge_id in EDGE_ORDER:
        spec = specs[edge_id]
        first = corners[spec["corners"][0]]
        second = corners[spec["corners"][1]]
        signs = [first["sign"], second["sign"]]
        tangent_axis = spec["varying_axis"]
        tangent_sign = dt if tangent_axis == "t" else dp
        need((tangent_sign > 0 and signs[0] <= signs[1]) or
             (tangent_sign < 0 and signs[0] >= signs[1]),
             edge_id + ": endpoint order agrees with strict derivative")
        common = {"edge_id": edge_id, "fixed_axis": spec["fixed_axis"],
                  "fixed_value": spec["fixed_value"],
                  "varying_axis": tangent_axis,
                  "exact_closed_interval": spec["varying_interval"],
                  "ordered_endpoint_signs": signs,
                  "ordered_endpoint_H1_intervals": [first["H1"], second["H1"]],
                  "strict_tangential_derivative_bounds": derivatives[tangent_axis],
                  "strict_tangential_derivative_sign": sign_name(tangent_sign)}
        if signs[0] != signs[1]:
            crossings.append(edge_id)
            root_id = "R_" + edge_id
            root = {"root_id": root_id, "edge_id": edge_id,
                    "definition": "THE_UNIQUE_H1_ZERO_ON_THE_OPEN_EDGE",
                    "fixed_axis": spec["fixed_axis"],
                    "fixed_value": spec["fixed_value"],
                    "varying_axis": tangent_axis,
                    "exact_isolating_open_interval": spec["varying_interval"],
                    "strict_opposite_endpoint_signs": signs,
                    "existence_by_IVT": True,
                    "uniqueness_by_uniform_strict_tangential_derivative": True,
                    "not_a_corner": True,
                    "projection_coordinate": projection_coordinate(edge_id, spec, root_id)}
            roots.append(root)
            edge_rows.append({**common, "edge_disposition": "ONE_UNIQUE_INTERIOR_H1_ZERO",
                              "root_id": root_id})
        else:
            edge_rows.append({**common,
                              "edge_disposition": "STRICT_NO_ZERO_" + sign_name(signs[0]),
                              "strict_whole_edge_sign": sign_name(signs[0]),
                              "root_id": None})
    need(len(crossings) == 2 and len(roots) == 2,
         "exactly two boundary incidences")
    slope_sign = -dp * dt
    low_root, high_root, order_proof = projection_order(crossings, specs, slope_sign)
    root_by_id = {row["root_id"]: row for row in roots}
    partition = {
        "H1_LT_0": "EXACT_OPEN_NEGATIVE_REGION_CUT_BY_CLIPPED_GRAPH",
        "H1_EQ_0": "EXACT_SINGLE_CLIPPED_REGULAR_GRAPH_ARC",
        "H1_GT_0": "EXACT_OPEN_POSITIVE_REGION_CUT_BY_CLIPPED_GRAPH",
        "pairwise_disjoint": True,
        "union_exact_child": True,
        "zero_carrier_has_exactly_two_boundary_endpoints": True,
        "zero_carrier_has_no_corner_incidence": True,
        "graph_full_dimensional_Kraft_weight": "0",
        "half_open_negative_owner": {"predicate": "H1<=0", "owns_graph": True},
        "half_open_positive_owner": {"predicate": "H1>0", "owns_graph": False},
    }
    arrangement = {
        "kind": "EXACT_CLIPPED_MONOTONE_GRAPH_AND_TWO_OFF_GRAPH_REGIONS",
        "precision_bits": 384,
        "equation": "H1=n1_x^2-n1_y^2",
        "v2_child_certificate_sha256": digest(cert),
        "full_child_strict_derivatives": {
            "t": {"sign": sign_name(dt), "bounds": derivatives["t"]},
            "p": {"sign": sign_name(dp), "bounds": derivatives["p"]}},
        "four_strict_nonzero_corners": sorted(cert["strict_corner_records"],
                                               key=lambda x: (fraction_text(x["point"]["t"]),
                                                              fraction_text(x["point"]["p"]))),
        "corner_zero_incidence_count": 0,
        "boundary_edges": edge_rows,
        "boundary_root_count": 2,
        "boundary_roots": roots,
        "boundary_crossing_edge_ids": crossings,
        "clipped_graph": {
            "dependent_axis": "t", "projection_axis": "p",
            "uniform_nonzero_dependent_derivative": True,
            "implicit_graph_derivative_sign": sign_name(slope_sign),
            "exact_projection_domain": {
                "kind": "EXACT_CLOSED_INTERVAL_BETWEEN_UNIQUE_BOUNDARY_ROOT_PROJECTIONS",
                "lower_endpoint": root_by_id[low_root]["projection_coordinate"],
                "lower_root_id": low_root,
                "upper_endpoint": root_by_id[high_root]["projection_coordinate"],
                "upper_root_id": high_root,
                "strict_order_proof": order_proof},
            "fiber_zero_count_on_projection_domain": "EXACTLY_ONE",
            "fiber_zero_count_outside_projection_domain": "ZERO",
            "below_graph_H1_sign": sign_name(-dt),
            "above_graph_H1_sign": sign_name(dt),
            "lower_projection_exterior_H1_sign": sign_name(-dp),
            "upper_projection_exterior_H1_sign": sign_name(dp),
            "single_connected_arc": True,
            "no_closed_or_disconnected_zero_component": True},
        "closure_theorem": {
            "boundary_exhaustive": True,
            "projection_coverage": True,
            "fiber_uniqueness": True,
            "two_sides_strict": True,
            "coverage_and_mutual_exclusion": True,
            "reason": "STRICT_DT_GIVES_AT_MOST_ONE_ZERO_PER_P_FIBER;_STRICT_DP_MAKES_BOTH_T_BOUNDARY_TRACES_STRICT;_FOUR_EDGE_CENSUS_GIVES_ONE_EXACT_PROJECTION_INTERVAL_AND_TWO_ENDPOINTS"},
    }
    return arrangement, partition


def transformed_body(v2: dict[str, Any]) -> dict[str, Any]:
    for key, value in ZERO.items():
        need(v2[key] == value, "v2 row zero credit:" + key)
    need(v2["global_consumption_ready"] is False, "v2 row global boundary")
    disposition = v2["intersection_disposition"]
    base = {
        "schema": SCHEMA + ".arrangement-row",
        "v2_intersection_row_sha256": v2["row_sha256"],
        "C65_aggregate_leaf_row_sha256": v2["C65_aggregate_leaf_row_sha256"],
        "source_C61_aggregate_leaf_row_sha256": v2["source_C61_aggregate_leaf_row_sha256"],
        "pair_index": v2["pair_index"], "source_path": v2["source_path"],
        "child_path": v2["child_path"],
        "exact_representative_box": v2["exact_representative_box"],
        "v2_disposition": disposition,
        "global_consumption_ready": False,
        **ZERO,
    }
    if disposition == "BLOCKED_C69C_SOURCE_CAPABILITY_NOT_AVAILABLE":
        return {**base, "child_numeric_domain": False,
                "arrangement_disposition": disposition,
                "H1_full_box_closure": None, "three_strata_partition": None,
                "child_level_H1_full_box_closed": False,
                "consumer_review_ready": False,
                "remaining_blocker_codes": v2["remaining_blocker_codes"]}
    need(disposition in EXPECTED_CENSUS, "known v2 disposition")
    if disposition == "PROVED_CHILD_H1_ZERO_CONTACT__BOUNDARY_ARRANGEMENT_UNSEALED":
        closure, partition = clipped_certificate(v2)
        arrangement_disposition = "LOCAL_H1_CLIPPED_GRAPH_AND_TWO_OFF_GRAPH_REGIONS"
    else:
        need(v2["consumer_review_ready"] is True and
             v2["three_strata_partition"]["pairwise_disjoint"] is True and
             v2["three_strata_partition"]["union_exact_child"] is True,
             "v2 existing full-box closure")
        closure = {"kind": "INDEPENDENTLY_VERIFIED_C71_V2_FULL_BOX_CLOSURE_REPLAY",
                   "v2_method": v2["H1_child_certificate"]["accepted_full_box_method"],
                   "v2_child_certificate_sha256": digest(v2["H1_child_certificate"]),
                   "v2_three_strata_partition_sha256": digest(v2["three_strata_partition"])}
        partition = v2["three_strata_partition"]
        arrangement_disposition = disposition
    return {**base, "child_numeric_domain": True,
            "arrangement_disposition": arrangement_disposition,
            "H1_full_box_closure": closure, "three_strata_partition": partition,
            "child_level_H1_full_box_closed": True,
            "consumer_review_ready": True, "remaining_blocker_codes": []}


class RowWriter:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.open("xb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw,
                                compresslevel=9, mtime=0)
        self.count = 0
        self.sequence = hashlib.sha256()

    def write(self, body: dict[str, Any]) -> dict[str, Any]:
        row = {**body, "row_sha256": digest(body)}
        self.gz.write(canonical(row) + b"\n")
        self.sequence.update((row["row_sha256"] + "\n").encode("ascii"))
        self.count += 1
        return row

    def close(self) -> dict[str, Any]:
        self.gz.close()
        self.raw.close()
        return {"filename": self.path.name, "sha256": file_sha(self.path),
                "size": self.path.stat().st_size, "row_count": self.count,
                "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
                "order": "C71_V2_INTERSECTION_ROW_ORDER"}


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
         "terminal-byte replay:" + path.name)


def build(v2_stage: Path, output: Path) -> dict[str, Any]:
    contract, v2_result = load_gate(v2_stage.resolve())
    need(output.exists() and output.is_dir() and not output.is_symlink(),
         "fresh output directory")
    for name in (ROWS_NAME, RESULT_NAME, REPORT_NAME):
        need(not (output / name).exists() and not (output / name).is_symlink(),
             "fresh output:" + name)
    counts: Counter[str] = Counter()
    closed_numeric = 0
    writer = RowWriter(output / ROWS_NAME)
    try:
        for v2 in iter_gzip_rows(v2_stage / V2_NAMES["rows"]):
            counts[v2["intersection_disposition"]] += 1
            body = transformed_body(v2)
            closed_numeric += int(body["child_level_H1_full_box_closed"])
            writer.write(body)
    finally:
        descriptor = writer.close()
    need(writer.count == EXPECTED_TOTAL and dict(counts) == EXPECTED_CENSUS,
         "complete v2 census")
    need(closed_numeric == EXPECTED_NUMERIC, "all 33100 numeric children closed")
    result = {
        "schema": SCHEMA + ".result",
        "status": "PASS_C71B_EXACT_33100_CHILD_H1_FULL_BOX_CLOSURE__17654_CLIPPED_BOUNDARY_ARRANGEMENTS__134155_FAIL_CLOSED__ZERO_CREDIT",
        "producer_file_sha256": file_sha(SELF),
        "frozen_inputs": {
            "contract_object_sha256": CONTRACT_OBJECT_SHA256,
            "schemas_object_sha256": SCHEMAS_OBJECT_SHA256,
            "C71_v2_result_object_sha256": v2_result["object_sha256"],
            "C71_v2_independent_verification_object_sha256":
                contract["frozen_C71_v2_stage"]["verification_object_sha256"]},
        "coverage": {
            "C65_collision2_child_count": EXPECTED_TOTAL,
            "decision_source_child_count": EXPECTED_NUMERIC,
            "blocker_source_child_count": EXPECTED_TOTAL - EXPECTED_NUMERIC,
            "C71_v2_disposition_census": dict(sorted(counts.items())),
            "existing_v2_full_box_closure_child_count": EXPECTED_NUMERIC - EXPECTED_CLIPPED,
            "new_exact_clipped_arrangement_child_count": EXPECTED_CLIPPED,
            "child_level_H1_full_box_closed_count": closed_numeric,
            "partition_identity": "167255=33100+134155"},
        "proof_invariants": {
            "all_17654_have_strict_dt_and_dp": True,
            "all_17654_have_four_strict_nonzero_corners": True,
            "all_17654_have_exactly_two_unique_boundary_roots": True,
            "all_17654_have_one_exact_clipped_graph_and_two_strict_sides": True,
            "all_17654_partitions_pairwise_disjoint_and_cover_exact_child": True,
            "all_33100_numeric_children_have_full_box_H1_closure": True,
            "all_134155_nondecision_children_remain_fail_closed": True},
        "ledgers": {"arrangement_rows": descriptor},
        "candidate_is_authority": False, "global_consumption_ready": False,
        "runtime_canonical_pointer_or_seal_writes": False,
        **ZERO,
    }
    result["object_sha256"] = digest(result)
    exclusive_write(output / RESULT_NAME, canonical(result) + b"\n")
    report = ("# C71b v3 exact clipped H1 arrangement candidate\n\n"
              "Closed child-level H1 full-box proofs: 33,100/33,100.\n\n"
              "New clipped boundary arrangements: 17,654/17,654.\n\n"
              "C69c nondecision children remain fail-closed: 134,155.\n\n"
              "Formal/global/D02 credit remains zero pending the global consumer.\n")
    exclusive_write(output / REPORT_NAME, report.encode("ascii"))
    return result


def static_self_test() -> dict[str, Any]:
    tests = {
        "partition_exact": EXPECTED_NUMERIC + 134155 == EXPECTED_TOTAL,
        "clipped_plus_existing_exact": EXPECTED_CLIPPED + 15446 == EXPECTED_NUMERIC,
        "four_edges": len(EDGE_ORDER) == 4 and len(set(EDGE_ORDER)) == 4,
        "credit_lock": all(value == 0 for value in ZERO.values()),
        "old_skeleton_not_dependency": "skeleton_v1" not in " ".join(V2_NAMES.values()),
        "no_numeric_kernel_needed": "flint" not in sys.modules,
    }
    need(all(tests.values()), "static self-test")
    return {"schema": SCHEMA + ".static-self-test",
            "status": "PASS_6_OF_6_PARTITION_EDGE_PIN_AND_ZERO_CREDIT_TESTS",
            "tests": tests, "files_written": False,
            "global_consumption_ready": False, **ZERO}


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--v2-stage", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        if args.self_test:
            need(args.output is None, "self-test writes nothing")
            result = static_self_test()
        else:
            need(args.output is not None, "output required")
            result = build(args.v2_stage, args.output.resolve())
        print(canonical(result).decode("ascii"))
        return 0
    except (Reject, KeyError, TypeError, ValueError, OSError) as exc:
        print(canonical({"status": "REJECTED", "reason": str(exc)}).decode("ascii"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
