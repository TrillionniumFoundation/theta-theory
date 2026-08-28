#!/usr/bin/env python3
"""Independent structural audit of the Round277 active-graph partition.

This audit deliberately does not grant geometric or component credit.  It
checks that the published 32,416/252 split is an exact, duplicate-free
partition of the frozen 32,668-row depth-8 residual universe and emits a
deterministic zero-credit ledger for the accepted *candidate indices*.

The accepted-index ledger is not an independent dynamic-evaluator
recomputation and is not a substitute for positive-area face patches plus
two inward corridors.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import pickle
from fractions import Fraction as Q
from pathlib import Path

import cm2_round276_source_g_collar_region_face_binding_probe as r276
import cm2_round277_source_g_collar_common_face_match_probe as r277


HERE = Path(__file__).resolve().parent
SOURCE = (
    HERE
    / "cm2_round277_source_g_depth8_residual_indices_zero_credit.json.gz"
)
TAILS = (
    HERE
    / "cm2_round277_source_g_depth8_active_graph_remaining_tails_zero_credit.json.gz"
)
PROBE_RESULT = (
    HERE
    / "cm2_round277_source_g_depth8_residual_active_graph_strategy_probe_result.json"
)
ACCEPTED_LEDGER = (
    HERE
    / "cm2_round277_source_g_depth8_active_graph_accepted_side_indices_zero_credit.json.gz"
)
RESULT = (
    HERE
    / "cm2_round277_source_g_depth8_active_graph_partition_audit_result.json"
)


def load_gzip(path: Path) -> dict:
    return json.loads(gzip.decompress(path.read_bytes()))


def qstr(value: Q) -> str:
    return str(value)


def candidate_face_payload(candidate: tuple) -> list:
    a, b, signature_hash, chart, target, axis, coordinate, overlap = candidate
    return [
        a,
        b,
        signature_hash,
        chart,
        target,
        axis,
        qstr(coordinate),
        [[qstr(lower), qstr(upper)] for lower, upper in overlap],
    ]


def main() -> int:
    source = load_gzip(SOURCE)
    tails = load_gzip(TAILS)
    probe = json.loads(PROBE_RESULT.read_bytes())

    source_rows = source["rows"]
    source_indices = [row["candidate_index"] for row in source_rows]
    assert len(source_indices) == len(set(source_indices)) == 32_668
    assert source["depth8_residual_count"] == 32_668
    assert source["candidate_indices_sha256"] == r276.digest(source_indices)

    tail_rows = tails["rows"]
    tail_indices = [row["candidate_index"] for row in tail_rows]
    assert len(tail_indices) == len(set(tail_indices)) == 252
    assert tails["row_count"] == 252
    assert tails["candidate_indices_sha256"] == r276.digest(tail_indices)
    assert set(tail_indices) < set(source_indices)

    cache_path = Path("/tmp/cm2_round277_candidate_runtime_cache.pkl")
    if cache_path.exists():
        r277.CAND, r277.BOX, r277.TABLES = pickle.loads(
            cache_path.read_bytes()
        )
    else:
        r277.build()
    assert len(r277.CAND) == 330_724

    source_by_index = {
        row["candidate_index"]: row for row in source_rows
    }
    group_keys = set()
    for index in source_indices:
        candidate = r277.CAND[index]
        a, b, signature_hash, chart, target, axis, coordinate, overlap = candidate
        metadata = source_by_index[index]["depth4_classification"]
        assert metadata["candidate_index"] == index
        assert metadata["signature_sha256"] == signature_hash
        assert metadata["chart"] == chart
        assert metadata["owner_target"] == target
        assert metadata["axis"] == axis
        assert a != b and a in r277.BOX and b in r277.BOX
        assert all(lower < upper for lower, upper in overlap)
        key = (a, b, chart, target, axis, coordinate, overlap)
        assert key not in group_keys
        group_keys.add(key)
    assert len(group_keys) == 32_668

    for row in tail_rows:
        index = row["candidate_index"]
        assert row["requested_signature_sha256"] == r277.CAND[index][2]
        assert row["failclosed_normal_forms"]
        assert all(
            form[3].startswith("FAILCLOSED")
            for form in row["failclosed_normal_forms"]
        )

    tail_set = set(tail_indices)
    accepted_indices = [
        index for index in source_indices if index not in tail_set
    ]
    assert len(accepted_indices) == 32_416
    assert set(accepted_indices).isdisjoint(tail_set)
    assert set(accepted_indices) | tail_set == set(source_indices)
    assert probe["geometric_face_group_count"] == 32_668
    assert probe["candidate_disposition_census"] == {
        "EXACT_POSITIVE_MATCH_SIDE_FOUND": 32_416,
        "FAILCLOSED_ACTIVE_GRAPH_TAIL": 252,
    }
    assert (
        probe["remaining_tail_candidate_indices_sha256"]
        == r276.digest(tail_indices)
    )

    accepted_rows = []
    for index in accepted_indices:
        candidate = r277.CAND[index]
        accepted_rows.append(
            {
                "candidate_index": index,
                "requested_signature_sha256": candidate[2],
                "geometric_face_group_sha256": r276.digest(
                    candidate_face_payload(candidate)
                ),
                "source_round_pair": source_by_index[index][
                    "depth4_classification"
                ]["round_pair"],
                "probe_disposition": "ACTIVE_GRAPH_REQUESTED_SIDE_REPORTED",
                "component_edge_credit": 0,
            }
        )
    accepted_document = {
        "status": (
            "ROUND277_DEPTH8_ACTIVE_GRAPH_ACCEPTED_SIDE_INDEX_LEDGER__"
            "STRUCTURAL_AUDIT__ZERO_CREDIT"
        ),
        "row_count": len(accepted_rows),
        "candidate_indices_sha256": r276.digest(accepted_indices),
        "rows_sha256": r276.digest(accepted_rows),
        "rows": accepted_rows,
        "strict_warning": (
            "STRUCTURAL COMPLEMENT ONLY; DYNAMIC EVALUATOR, POSITIVE-AREA "
            "PATCH, AND TWO-CORRIDOR RECOMPUTATION ARE NOT PROVIDED"
        ),
    }
    accepted_bytes = (
        json.dumps(
            accepted_document, sort_keys=True, separators=(",", ":")
        )
        + "\n"
    ).encode()
    ACCEPTED_LEDGER.write_bytes(
        gzip.compress(accepted_bytes, compresslevel=9, mtime=0)
    )

    active_histogram = probe["active_normal_form_histogram"]
    exact_zero_rows = {
        key: count
        for key, count in active_histogram.items()
        if "EXACT_ZERO" in key
    }
    assert exact_zero_rows
    assert all(
        key.split("|")[2].split(",")[-1] == "EXACT_ZERO"
        for key in exact_zero_rows
    )

    result = {
        "status": (
            "ROUND277_DEPTH8_ACTIVE_GRAPH_PARTITION_STRUCTURAL_AUDIT__"
            "PASS_ZERO_CREDIT"
        ),
        "source_residual_count": 32_668,
        "source_residual_candidate_indices_sha256": r276.digest(
            source_indices
        ),
        "geometric_face_group_count": len(group_keys),
        "accepted_side_index_count": len(accepted_indices),
        "accepted_side_candidate_indices_sha256": r276.digest(
            accepted_indices
        ),
        "failclosed_tail_count": len(tail_indices),
        "failclosed_tail_candidate_indices_sha256": r276.digest(
            tail_indices
        ),
        "partition_is_exact_duplicate_free_and_exhaustive": True,
        "one_candidate_per_geometric_face_group": True,
        "all_face_overlaps_have_two_strictly_positive_tangent_widths": True,
        "exact_zero_normal_forms_are_always_in_second_tangent_coordinate": True,
        "accepted_ledger": ACCEPTED_LEDGER.name,
        "accepted_ledger_file_sha256": hashlib.sha256(
            ACCEPTED_LEDGER.read_bytes()
        ).hexdigest(),
        "accepted_ledger_rows_sha256": accepted_document["rows_sha256"],
        "strict_scope": [
            "PARTITION_AND_FROZEN_CANDIDATE_IDENTITY_ONLY",
            "NO_INDEPENDENT_DYNAMIC_EVALUATOR_RECOMPUTATION",
            "NO_POSITIVE_AREA_PATCH_RADIUS_MATERIALIZATION",
            "NO_TWO_INWARD_CORRIDOR_MATERIALIZATION",
            "NO_COMPONENT_OR_MAXIMALITY_CREDIT",
        ],
        "strict_nonpromotion": {
            "expanded_occurrence_credit": 0,
            "component_edge_credit": 0,
            "rank_reduction_credit": 0,
            "maximality_credit": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    RESULT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
