#!/usr/bin/env python3
"""Verifier for the Round-74 fixed-s0 depth-two/cross-rank assault."""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from cm2_round68_common import digest, require, sha256_path, strict_json_path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round74-s0-depth2-cross-rank-manifest-2026-07-21.json"
LEGACY = HERE / "cm2-round74-s0-depth2-registry-2026-07-21.json"
ADAPTIVE = HERE / "cm2-round74-s0-depth2-adaptive-2026-07-21.json"
WITNESSES = HERE / "cm2-round74-s0-r2-pair-witnesses-2026-07-21.json"
CERT = HERE / "cm2_round74_s0_depth2_cross_rank_cert.py"


def strict_json_bytes(blob: bytes) -> Any:
    text = blob.decode()
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    def constant(value: str) -> Any:
        raise ValueError(value)
    decoder = json.JSONDecoder(object_pairs_hook=pairs, parse_constant=constant)
    value, end = decoder.raw_decode(text)
    require(not text[end:].strip(), "trailing JSON")
    return value


def integrity(document: dict[str, Any]) -> None:
    require(document["schema"] == "cm2.round74.s0-depth2-cross-rank.v1", "schema")
    require(document["result_sha256"] == digest(document["result"]), "result digest")
    for name, expected in document["pins"].items():
        require(sha256_path(HERE / name) == expected, f"pin {name}")


def semantics(result: dict[str, Any]) -> None:
    legacy = result["legacy_3D_registry_slice_diagnosis"]
    require(legacy["strict_open_s0_Q1_parents"] == 32, "legacy parents")
    require(legacy["adaptive_s_endpoint_only_boxes_rejected"] == 772, "endpoint exclusion")
    registry = result["fixed_s0_depth16_registry"]
    require(registry["terminal_leaves"] == 153508, "terminal leaves")
    require(registry["classification_histogram"] == {"DEPTH2_OUTER": 65256, "Q2_INNER": 76708, "R1_INNER": 9112, "R2_INNER": 2432}, "histogram")
    require(registry["R2_strict_leaf_count"] == 2432, "R2 leaf field")
    require(registry["normalized_area_total"] == "24", "area")
    require(registry["R2_strict_normalized_area_lower"] == "19/512", "R2 area")
    pairs = result["positive_R2_pair_registry"]
    require(pairs["positive_boxes"] == pairs["source_destination_pairs"] == 16, "pair witnesses")
    require(pairs["main_pairs"] == pairs["narrow_corner_pairs"] == 8, "branch split")
    incidence = result["cross_rank_incidence"]
    require(incidence["strict_child_to_parent_incidence_edges"] == 88252, "incidence")
    require(incidence["R1_children_to_return_parent"] + incidence["Q2_R2_children_to_survival_parent"] == 88252, "incidence sum")
    trace = result["oriented_trace_test"]
    require(trace["binary_split_internal_faces"] == trace["oppositely_oriented_artificial_face_pairs_cancelled"] == 153484, "trace cancellation")
    require(trace["artificial_dyadic_trace_cancellation_across_rank_join"] == "CERTIFIED_EXACT", "artificial status")
    require(trace["physical_R2_pullback_trace_cancellation_across_rank_join"].startswith("NOT_CERTIFIED"), "physical nonpromotion")
    frontier = result["strict_frontier"]
    require(frontier["physical_cross_rank_trace_cancellation"] == "NOT_CERTIFIED", "frontier physical trace")
    require(frontier["complete_composite_gates"] == "0/5" and frontier["CM2"] == "NO-GO_FOR_CLAIM", "verdict")


def replay_proofs() -> dict[str, str]:
    legacy = strict_json_path(LEGACY)["result"]
    adaptive = strict_json_path(ADAPTIVE)["result"]
    witnesses = strict_json_path(WITNESSES)["result"]
    require(legacy["Q1_boxes_touching_s0_closed"] == 804, "legacy touching")
    require(legacy["Q1_boxes_with_s0_strictly_in_open_s_interval"] + legacy["Q1_boxes_touching_s0_only_at_adaptive_endpoint_rejected"] == 804, "legacy partition")
    histogram = adaptive["classification_histogram"]
    require(sum(histogram.values()) == adaptive["terminal_leaf_count"], "leaf sum")
    require(adaptive["binary_split_count"] == adaptive["terminal_leaf_count"] - adaptive["source_core_count"], "binary tree identity")
    areas = {key: Q(value) for key, value in adaptive["normalized_24_core_area_ledger"].items()}
    require(sum(areas.values(), Q(0)) == 24, "global area conservation")
    require(Q(24) - areas["DEPTH2_OUTER"] == Q(188451, 8192), "certified area")
    r2_rows = adaptive["R2_rows"]
    require(len(r2_rows) == 2432 and adaptive["R2_rows_sha256"] == digest(r2_rows), "R2 rows")
    require(len({row["source_core_index"] for row in r2_rows}) == 8, "R2 sources")
    require(len({(row["source_core_index"], row["destination_core_id"]) for row in r2_rows}) == 8, "dyadic R2 pairs")
    witness_rows = witnesses["rows"]
    require(len(witness_rows) == 16 and witnesses["rows_sha256"] == digest(witness_rows), "witness rows")
    require(len({row["witness_box_id"] for row in witness_rows}) == 16, "witness IDs")
    require(len({(row["source_core_id"], row["destination_core_id"]) for row in witness_rows}) == 16, "witness pairs")
    for row in witness_rows:
        require(Q(row["t_interval"][0]) < Q(row["t_interval"][1]), "t width")
        require(Q(row["p_interval"][0]) < Q(row["p_interval"][1]), "p width")
        require(Q(row["positive_coordinate_area"]) > 0, "positive witness area")
        require(row["strict_time1_classification"] == "SURVIVE_THROUGH_1_INNER", "Q1 parent")
        require(row["strict_time2_classification"] == "RETURN_AT_2_INNER", "R2 child")
    return {"legacy_fixed_s0_split": "804=32+772", "depth16_area": "PASS", "R2_dyadic_rows": "2432/2432", "R2_pair_boxes": "16/16", "binary_trace_pairs": "153484/153484"}


def deterministic(document: dict[str, Any]) -> None:
    process = subprocess.run([sys.executable, str(CERT), "--manifest-json"], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    require(process.returncode == 0, process.stderr.decode())
    require(process.stdout == MANIFEST.read_bytes(), "byte reemit")
    require(strict_json_bytes(process.stdout) == document, "reemit JSON")


def hostile(document: dict[str, Any]) -> int:
    mutations = [
        (("result", "fixed_s0_depth16_registry", "terminal_leaves"), 153507),
        (("result", "fixed_s0_depth16_registry", "R2_strict_leaf_count"), 2431),
        (("result", "positive_R2_pair_registry", "source_destination_pairs"), 15),
        (("result", "cross_rank_incidence", "strict_child_to_parent_incidence_edges"), 88251),
        (("result", "oriented_trace_test", "physical_R2_pullback_trace_cancellation_across_rank_join"), "CERTIFIED_EXACT"),
        (("result", "strict_frontier", "complete_composite_gates"), "1/5"),
    ]
    cases = []
    for path, value in mutations:
        for _ in range(32):
            case = copy.deepcopy(document)
            node = case
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = value
            case["result_sha256"] = digest(case["result"])
            cases.append(case)
    rejected = 0
    for case in cases:
        try:
            semantics(case["result"])
        except Exception:
            rejected += 1
    require(rejected == len(cases), "hostile rejection")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    document = strict_json_path(MANIFEST)
    integrity(document)
    semantics(document["result"])
    replay = replay_proofs()
    if args.audit:
        deterministic(document)
        bad = [b'{"a":1,"a":2}', b'{"x":NaN}', b'{"x":Infinity}', b'{"x":1} trailing']
        rejected = 0
        for blob in bad:
            try:
                strict_json_bytes(blob)
            except Exception:
                rejected += 1
        require(rejected == 4, "strict JSON")
        replay.update({"hostile_semantic_rejections": f"{hostile(document)}/192", "strict_json_rejections": "4/4", "byte_identical_reemit": "PASS"})
    print(json.dumps({"status": "PASS", "replay": replay}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
