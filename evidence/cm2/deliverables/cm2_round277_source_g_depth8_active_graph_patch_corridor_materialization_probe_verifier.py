#!/usr/bin/env python3
"""Independent geometric verifier for the Round277 depth-8 witness probe."""
from __future__ import annotations

import collections
import gzip
import hashlib
import json
import multiprocessing as mp
import pickle
from fractions import Fraction as Q
from pathlib import Path

from flint import ctx

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round276_source_g_collar_region_face_binding_probe as r276
import cm2_round277_source_g_collar_common_face_match_probe as r277


HERE = Path(__file__).resolve().parent
LEDGER = (
    HERE
    / "cm2_round277_source_g_depth8_active_graph_face_edge_witnesses_zero_credit.json.gz"
)
RESIDUAL = (
    HERE / "cm2_round277_source_g_depth8_residual_indices_zero_credit.json.gz"
)
ROWS = []


def load():
    global ROWS
    cache = Path("/tmp/cm2_round277_candidate_runtime_cache.pkl")
    if cache.exists():
        r277.CAND, r277.BOX, r277.TABLES = pickle.loads(cache.read_bytes())
    else:
        r277.build()
    ledger = json.loads(gzip.decompress(LEDGER.read_bytes()))
    residual = json.loads(gzip.decompress(RESIDUAL.read_bytes()))
    ROWS = ledger["rows"]
    expected = [row["candidate_index"] for row in residual["rows"]]
    actual = [row["candidate_index"] for row in ROWS]
    assert len(expected) == len(actual) == 32668
    assert actual == sorted(actual)
    assert actual == expected
    assert len(set(actual)) == len(actual)
    assert ledger["row_count"] == len(actual)
    assert ledger["candidate_indices_sha256"] == r276.digest(actual)
    assert ledger["rows_sha256"] == r276.digest(ROWS)
    return ledger


def signature_hash(chart, target, values, label):
    box = r174.atlas.AtlasBox(*values, 0, label)
    signature, rejected = r174.dynamic_signature(
        chart, box, target, r277.TABLES
    )
    if signature is None:
        return None, tuple(rejected)
    return r276.digest(r277.payload(signature, chart)), ()


def inside(values, bounds):
    return all(
        bounds[2 * axis] <= values[2 * axis]
        <= values[2 * axis + 1]
        <= bounds[2 * axis + 1]
        for axis in range(3)
    )


def worker(row_index):
    row = ROWS[row_index]
    i = row["candidate_index"]
    a, b, expected, chart, target, axis, coordinate, overlap = r277.CAND[i]
    patch = list(map(Q, row["exact_positive_area_face_patch"]))
    if patch[2 * axis] != coordinate or patch[2 * axis + 1] != coordinate:
        return "FAIL_FACE_COORDINATE"
    j = 0
    for k in range(3):
        if k == axis:
            continue
        lower, upper = overlap[j]
        if not (
            lower <= patch[2 * k] < patch[2 * k + 1] <= upper
        ):
            return "FAIL_POSITIVE_TANGENTIAL_PATCH_OR_CONTAINMENT"
        j += 1
    actual, rejected = signature_hash(
        chart, target, patch, f"round277-independent-face:{i}"
    )
    if actual != expected:
        return "FAIL_FACE_SIGNATURE"
    corridors = row["two_inward_corridors"]
    if len(corridors) != 2:
        return "FAIL_CORRIDOR_COUNT"
    if {item["leaf_row_id"] for item in corridors} != {a, b}:
        return "FAIL_CORRIDOR_LEAF_SET"
    sides = collections.Counter()
    for item in corridors:
        leaf_id = item["leaf_row_id"]
        bounds = r277.BOX[leaf_id]
        values = list(map(Q, item["exact_corridor_box"]))
        if not inside(values, bounds):
            return "FAIL_CORRIDOR_CONTAINMENT"
        for k in range(3):
            if k != axis and values[2 * k : 2 * k + 2] != patch[
                2 * k : 2 * k + 2
            ]:
                return "FAIL_TANGENTIAL_PATCH_MISMATCH"
        negative = bounds[2 * axis + 1] == coordinate
        positive = bounds[2 * axis] == coordinate
        if negative == positive:
            return "FAIL_FACE_ORIENTATION"
        if negative:
            if not (
                values[2 * axis] < values[2 * axis + 1] == coordinate
            ):
                return "FAIL_NEGATIVE_INWARD_CORRIDOR"
            expected_side = "NEGATIVE_SIDE_INWARD"
        else:
            if not (
                coordinate == values[2 * axis]
                < values[2 * axis + 1]
            ):
                return "FAIL_POSITIVE_INWARD_CORRIDOR"
            expected_side = "POSITIVE_SIDE_INWARD"
        if item["geometric_side"] != expected_side:
            return "FAIL_SIDE_LABEL"
        sides[expected_side] += 1
        actual, rejected = signature_hash(
            chart, target, values, f"round277-independent-corridor:{i}"
        )
        if actual != expected:
            return "FAIL_CORRIDOR_SIGNATURE"
    if sides != {
        "NEGATIVE_SIDE_INWARD": 1,
        "POSITIVE_SIDE_INWARD": 1,
    }:
        return "FAIL_TWO_SIDED_ORIENTATION"
    classification = row["witness_classification"]
    if classification == "PASS_P_ENDPOINT_WEDGE_PATCH_AND_TWO_CORRIDORS":
        if axis != 2 or Q(row["p_endpoint"]) not in {Q(-1), Q(1)}:
            return "FAIL_ENDPOINT_WEDGE_IDENTITY"
        endpoint = Q(row["p_endpoint"])
        if endpoint not in {patch[2], patch[3]} or patch[2] == patch[3]:
            return "FAIL_ENDPOINT_WEDGE_PATCH"
    elif classification != "PASS_REGULAR_ACTIVE_SIDE_PATCH_AND_TWO_CORRIDORS":
        return "FAIL_WITNESS_CLASSIFICATION"
    return "PASS"


def main():
    ctx.prec = 256
    ledger = load()
    counts = collections.Counter()
    with mp.get_context("fork").Pool(min(40, mp.cpu_count())) as pool:
        for status in pool.imap_unordered(worker, range(len(ROWS)), chunksize=16):
            counts[status] += 1
    assert counts == {"PASS": 32668}, counts
    result = {
        "status": "PASS_INDEPENDENT_ROUND277_DEPTH8_ACTIVE_GRAPH_PATCH_CORRIDOR_PROBE__ZERO_CREDIT",
        "verified_witness_row_count": len(ROWS),
        "verified_face_patch_count": len(ROWS),
        "verified_corridor_count": 2 * len(ROWS),
        "witness_classification_histogram": dict(
            sorted(
                collections.Counter(
                    row["witness_classification"] for row in ROWS
                ).items()
            )
        ),
        "verification_histogram": dict(sorted(counts.items())),
        "witness_rows_sha256": ledger["rows_sha256"],
        "witness_ledger_file_sha256": hashlib.sha256(
            LEDGER.read_bytes()
        ).hexdigest(),
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    output = (
        HERE
        / "cm2_round277_source_g_depth8_active_graph_patch_corridor_materialization_probe_verification.json"
    )
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
