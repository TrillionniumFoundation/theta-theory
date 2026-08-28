#!/usr/bin/env python3
"""Verifier for the Round-75 physical R2 depth-two subquotient."""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from typing import Any

from cm2_round68_common import digest, require, sha256_path, strict_json_path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round75-r2-physical-subquotient-manifest-2026-07-21.json"
CURVES = HERE / "cm2-round75-r2-physical-curves-2026-07-21.json"
NONINTERSECTION = HERE / "cm2-round75-r2-curve-nonintersection-2026-07-21.json"
CERT = HERE / "cm2_round75_r2_physical_subquotient_cert.py"


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
    require(document["schema"] == "cm2.round75.r2-physical-subquotient.v1", "schema")
    require(document["result_sha256"] == digest(document["result"]), "result digest")
    for name, expected in document["pins"].items():
        require(sha256_path(HERE / name) == expected, f"pin {name}")


def semantics(result: dict[str, Any]) -> None:
    atlas = result["physical_R2_curve_atlas"]
    require((atlas["certified_components"], atlas["physical_curves"], atlas["stationary_endpoint_vertices"]) == (16, 32, 64), "atlas counts")
    require(atlas["main_components"] == atlas["narrow_corner_components"] == 8, "branch counts")
    require(atlas["source_cores"] == 8 and atlas["parametric_interval_Newton_slabs"] == 4096, "atlas coverage")
    require(atlas["time_j"] == 2 and atlas["physical_second_collision_owner"] == "W[0,0]", "physical owner")
    owner = result["owner_chart_qualification"]
    require(owner["strict_Q1_owner_destination_chart_other_coordinate_on_all_curves"], "owner/chart qualification")
    require((owner["curves_using_chart_free_candidate_union_on_at_least_one_slab"], owner["curves_using_chart_free_candidate_union_on_every_slab"], owner["chart_free_candidate_union_slabs"]) == (16, 8, 1360), "chart-free counts")
    require(owner["scan_bisection_fallback_slabs"] == 0, "root fallback")
    nonintersection = result["physical_curve_nonintersection"]
    require((nonintersection["source_cores"], nonintersection["all_pairs_per_source_core"], nonintersection["certified_nonintersecting_pairs"]) == (8, 48, 48), "nonintersection counts")
    require(nonintersection["unresolved"] == 0 and nonintersection["maximum_binary_depth"] == 21, "nonintersection completion")
    quotient = result["depth_two_physical_subquotient"]
    require(quotient["base_R1_f_vector"] == [144, 160, 40], "base f-vector")
    require(quotient["f_vector"] == [208, 256, 72], "subquotient f-vector")
    require(quotient["f_vector"][0] - quotient["f_vector"][1] + quotient["f_vector"][2] == quotient["connected_physical_core_rectangles"] == 24, "Euler")
    require((quotient["stationary_segments_after_R2_subdivision"], quotient["R1_plus_R2_physical_pullback_edges"]) == (192, 64), "edge partition")
    require((quotient["certified_R1_cells"], quotient["certified_R2_band_cells"], quotient["residual_complement_cells"]) == (16, 16, 40), "cell partition")
    require(quotient["residual_cells_are_not_promoted_to_Q2"], "residual nonpromotion")
    incidence = result["cross_rank_incidence"]
    require((incidence["R2_component_to_Round73_survival_parent_edges"], incidence["R2_curve_to_parent_incidence_edges"], incidence["R2_one_sided_trace_records"]) == (16, 32, 64), "incidence")
    trace = result["oriented_physical_trace_cancellation"]
    require((trace["Round73_internal_R1_pullback_edges"], trace["Round75_internal_R2_pullback_edges"], trace["internal_physical_pullback_edges"]) == (32, 32, 64), "trace edge counts")
    require(trace["oppositely_oriented_physical_trace_pairs_cancelled"] == 64 and trace["duplicate_trace_cost_before_total_variation"] == 0, "physical trace cancellation")
    require(trace["status"] == "CERTIFIED_EXACT_ON_THE_72_CELL_DEPTH2_SUBQUOTIENT", "trace scope")
    attack = result["F14_F15_F17_attack"]
    require(attack["F17_boundary_sector"].startswith("CERTIFIED_DEPTH2_SUBQUOTIENT"), "F17 boundary")
    require(attack["F17_official"] == "NOT_CERTIFIED", "F17 official nonpromotion")
    frontier = result["strict_frontier"]
    require(frontier["complete_fixed_s0_depth2_physical_face_atlas"].startswith("NOT_CERTIFIED"), "atlas frontier")
    require(frontier["Gate4"] == "NOT_CERTIFIED__LANDING_JOIN_1_OF_7", "Gate4")
    require(frontier["Gate5"] == "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0", "Gate5")
    require(frontier["complete_composite_gates"] == "0/5" and frontier["CM2"] == "NO-GO_FOR_CLAIM", "verdict")


def replay_curves() -> dict[str, str]:
    curves = strict_json_path(CURVES)
    require(curves["schema"] == "cm2.round75.r2-physical-curves.v1", "curve schema")
    result = curves["result"]
    component_rows = result["component_rows"]
    curve_rows = result["curve_rows"]
    require(len(component_rows) == 16 and result["component_rows_sha256"] == digest(component_rows), "component rows")
    require(len(curve_rows) == 32 and result["curve_rows_sha256"] == digest(curve_rows), "curve rows")
    require(len({row["curve_id"] for row in curve_rows}) == 32, "curve IDs")
    component_curve_ids = [curve_id for row in component_rows for curve_id in row["physical_curve_ids"]]
    require(len(component_curve_ids) == 32 and set(component_curve_ids) == {row["curve_id"] for row in curve_rows}, "component/curve join")
    require(sum(row["branch"] == "main" for row in component_rows) == 8, "main components")
    require(sum(row["branch"] == "narrow_corner" for row in component_rows) == 8, "narrow components")
    source_groups: dict[int, list[str]] = {}
    chart_free_curves = 0
    fully_chart_free_curves = 0
    chart_free_slabs = 0
    fallback_slabs = 0
    for row in curve_rows:
        source_groups.setdefault(row["source_core_index"], []).append(row["curve_id"])
        require(row["parametric_interval_newton_slab_count"] == 128, "slabs per curve")
        require(row["slabs_sha256"] == digest(row["slabs"]), "slab digest")
        require(row["endpoint_on_source_t_side"]["signs"][0] * row["endpoint_on_source_t_side"]["signs"][1] == -1, "t-side endpoint bracket")
        require(row["endpoint_on_source_p_side"]["signs"][0] * row["endpoint_on_source_p_side"]["signs"][1] == -1, "p-side endpoint bracket")
        p_endpoint = [Q(value) for value in row["endpoint_on_source_t_side"]["p_interval"]]
        t_endpoint = [Q(value) for value in row["endpoint_on_source_p_side"]["t_interval"]]
        require(p_endpoint[0] < p_endpoint[1] and t_endpoint[0] < t_endpoint[1], "endpoint interval")
        slabs = row["slabs"]
        require([slab["index"] for slab in slabs] == list(range(128)), "slab indices")
        for index, slab in enumerate(slabs):
            require(slab["interval_newton_strict_interior"] and slab["dt_level_sign"] in (-1, 1), "interval Newton")
            require(slab["root_location_method"] in ("continued_newton", "scan_bisection_fallback"), "root method")
            p_interval = [Q(value) for value in slab["p_interval"]]
            t_interval = [Q(value) for value in slab["interval_newton_t_interval"]]
            require(p_interval[0] < p_interval[1] and t_interval[0] < t_interval[1], "slab interval")
            if index:
                previous = {Q(value) for value in slabs[index - 1]["p_interval"]}
                require(bool(previous.intersection(p_interval)), "slab continuity")
        flags = [slab["chart_free_owner_union_used"] for slab in slabs]
        chart_free_curves += any(flags)
        fully_chart_free_curves += all(flags)
        chart_free_slabs += sum(flags)
        fallback_slabs += sum(slab["root_location_method"] == "scan_bisection_fallback" for slab in slabs)
    require(len(source_groups) == 8 and all(len(ids) == 4 for ids in source_groups.values()), "four curves per source")
    require(sum(len(row["slabs"]) for row in curve_rows) == result["parametric_interval_newton_slab_count"] == 4096, "slab total")
    require((chart_free_curves, fully_chart_free_curves, chart_free_slabs, fallback_slabs) == (16, 8, 1360, 0), "owner mode replay")
    return {"physical_R2_components": "16/16", "physical_R2_curves": "32/32", "endpoint_brackets": "64/64", "interval_Newton_slabs": "4096/4096"}


def replay_nonintersection() -> dict[str, str]:
    curves = strict_json_path(CURVES)["result"]["curve_rows"]
    proof = strict_json_path(NONINTERSECTION)
    require(proof["schema"] == "cm2.round75.r2-curve-nonintersection.v1", "nonintersection schema")
    result = proof["result"]
    rows = result["rows"]
    require(len(rows) == 48 and result["rows_sha256"] == digest(rows), "nonintersection rows")
    groups: dict[int, list[str]] = {}
    for curve in curves:
        groups.setdefault(curve["source_core_index"], []).append(curve["curve_id"])
    expected_pairs = {
        (source, *sorted(pair))
        for source, curve_ids in groups.items()
        for pair in combinations(curve_ids, 2)
    }
    actual_pairs = {(row["source_core_index"], *sorted((row["left_curve_id"], row["right_curve_id"]))) for row in rows}
    require(actual_pairs == expected_pairs and len(actual_pairs) == 48, "all source-core pairs")
    require(all(row["unresolved_count"] == 0 for row in rows), "pair unresolved")
    require(sum(row["box_tests"] for row in rows) == result["total_box_tests"] == 24752, "box tests")
    require(sum(row["excluded_leaf_count"] for row in rows) == result["total_excluded_leaves"] == 12400, "excluded leaves")
    require(max(row["maximum_depth"] for row in rows) == result["global_maximum_depth"] == 21, "maximum depth")
    return {"all_source_core_curve_pairs": "48/48", "unresolved_intersections": "0"}


def deterministic(document: dict[str, Any]) -> None:
    process = subprocess.run([sys.executable, str(CERT), "--manifest-json"], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    require(process.returncode == 0, process.stderr.decode())
    require(process.stdout == MANIFEST.read_bytes(), "byte reemit")
    require(strict_json_bytes(process.stdout) == document, "reemit JSON")


def hostile(document: dict[str, Any]) -> int:
    mutations = [
        (("result", "physical_R2_curve_atlas", "physical_curves"), 31),
        (("result", "owner_chart_qualification", "chart_free_candidate_union_slabs"), 1359),
        (("result", "physical_curve_nonintersection", "certified_nonintersecting_pairs"), 47),
        (("result", "depth_two_physical_subquotient", "f_vector"), [208, 255, 72]),
        (("result", "oriented_physical_trace_cancellation", "oppositely_oriented_physical_trace_pairs_cancelled"), 63),
        (("result", "F14_F15_F17_attack", "F17_official"), "CERTIFIED"),
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
    replay = replay_curves()
    replay.update(replay_nonintersection())
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
        replay.update({"hostile_semantic_rejections": f"{hostile(document)}/224", "strict_json_rejections": "4/4", "byte_identical_reemit": "PASS"})
    print(json.dumps({"status": "PASS", "replay": replay}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
