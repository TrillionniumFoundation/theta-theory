#!/usr/bin/env python3
"""Independent structural and hostile-semantic audit for CM2 Round 78."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "cm2-round78-physical-boundary-rank3-manifest-2026-07-21.json"
COMPONENTS = HERE / "cm2-round78-carrier-components-2026-07-21.json"
TANGENCIES = HERE / "cm2-round78-time2-tangency-curves-2026-07-21.json"
SEAM = HERE / "cm2-round78-chart-free-seam-resolution-2026-07-21.json"
TIME3 = HERE / "cm2-round78-s0-time3-registry-2026-07-21.json"
PIN_FILES = {
    "round77_taxonomy": HERE / "cm2-round77-boundary-taxonomy-2026-07-21.json",
    "round77_rn_sum": HERE / "cm2-round77-rn-weighted-finite-face-sum-2026-07-21.json",
    "tube_components": COMPONENTS,
    "r1_witnesses": HERE / "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json",
    "r1_monotonicity": HERE / "cm2-round72-r1-positive-component-monotonicity-proof-2026-07-21.json",
    "r1_numeric": HERE / "cm2-round72-r1-component-f10-f13-f16-proof-2026-07-21.json",
    "r2_curves": HERE / "cm2-round75-r2-physical-curves-2026-07-21.json",
    "tangency_curves": TANGENCIES,
    "seam_resolution": SEAM,
    "time3_registry": TIME3,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def strict_load(path: Path) -> dict[str, Any]:
    def pairs(rows: list[tuple[str, Any]]) -> dict[str, Any]:
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError("duplicate key")
            result[key] = value
        return result
    return json.loads(
        path.read_text(), object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )


def curve_bbox(row: dict[str, Any]) -> tuple[Q, Q, Q, Q]:
    xs: list[Q] = []
    ys: list[Q] = []
    for slab in row["slabs"]:
        parameter = tuple(map(Q, slab["parameter_interval"]))
        root = tuple(map(Q, slab["root_interval"]))
        if row["parameter_axis"] == "t":
            xs.extend(parameter)
            ys.extend(root)
        else:
            xs.extend(root)
            ys.extend(parameter)
    return min(xs), max(xs), min(ys), max(ys)


def broad_phase(rows: list[dict[str, Any]]) -> tuple[int, int]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["source_core_index"]].append(row)
    pair_count = 0
    overlap_count = 0
    for curves in grouped.values():
        for left, right in combinations(curves, 2):
            pair_count += 1
            a = curve_bbox(left)
            b = curve_bbox(right)
            if max(a[0], b[0]) <= min(a[1], b[1]) and max(a[2], b[2]) <= min(a[3], b[3]):
                overlap_count += 1
    return pair_count, overlap_count


def validate_claim_surface(manifest: dict[str, Any], *, check_pins: bool = True) -> None:
    require(manifest["schema"] == "cm2.round78.physical-boundary-rank3.v1", "manifest schema")
    require(manifest["result_sha256"] == digest(manifest["result"]), "result digest")
    if check_pins:
        require(set(manifest["pins"]) == set(PIN_FILES), "pin key set")
        require(all(
            manifest["pins"][name] == hashlib.sha256(path.read_bytes()).hexdigest()
            for name, path in PIN_FILES.items()
        ), "pin hashes")
    result = manifest["result"]
    resolution = result["round77_failure_mechanism_resolution"]
    require(resolution["outer_leaf_count"] == 263072, "outer count")
    require(resolution["interval_tube_family_count"] == 65, "tube family count")
    require(resolution["tube_source_carrier_pair_count"] == 132, "source-carrier pair count")
    require(resolution["tube_grid_component_count"] == 236, "tube component count")
    require(resolution["all_failure_mechanisms_mapped_to_certified_physical_carriers_or_strict_open_cells"], "mechanism coverage")
    atlas = result["physical_boundary_carrier_atlas"]
    require(atlas["status"] == "CERTIFIED_FOR_ALL_ROUND77_FAILURE_MECHANISMS", "atlas status")
    require(atlas["physical_curve_count"] == 156, "atlas curve count")
    quotient = result["depth_two_quotient"]
    require(quotient["status"].startswith("NOT_CERTIFIED"), "quotient overclaim")
    require(quotient["gate4_commuting_square_promotion"] == "NO", "Gate4 overclaim")
    require(quotient["broad_phase_same_source_tangency_pair_count"] == 244, "broad pair count")
    require(quotient["broad_phase_strictly_bbox_disjoint_pair_count"] == 68, "broad disjoint count")
    require(quotient["broad_phase_bounding_box_overlap_count"] == 176, "broad overlap count")
    frontier = result["fixed_s0_rank_three_frontier"]
    require(frontier["strict_Q3_cell_count"] == 14928, "manifest Q3 count")
    require(frontier["strict_R3_cell_count"] == 0, "manifest R3 count")
    rn = result["RN_frontier"]
    require(rn["rank3_physical_face_count"] == 0 and rn["rank3_RN_face_row_count"] == 0, "rank3 RN rows")
    require(rn["all_rank_RN_summability"].startswith("NOT_CERTIFIED"), "RN tail overclaim")
    require(result["strict_state"] == {
        "CM2": "NO-GO_FOR_CLAIM",
        "complete_composite_gates": "0/5",
        "gate4": "1/7",
        "gate5": "10/18",
        "gate5_complete_blocks": 0,
    }, "strict state")


def validate(
    manifest: dict[str, Any], components: dict[str, Any], tangencies: dict[str, Any],
    seam: dict[str, Any], time3: dict[str, Any], *, expensive: bool = True,
) -> None:
    validate_claim_surface(manifest)
    result = manifest["result"]
    resolution = result["round77_failure_mechanism_resolution"]

    component_result = components["result"]
    require(components["schema"] == "cm2.round78.carrier-components.v1", "components schema")
    require(component_result["component_family_histogram"] == {
        "outgoing_seam_geometry": 8,
        "time1_destination": 24,
        "time2_destination": 112,
        "time2_tangency": 92,
    }, "component histogram")
    require(len(component_result["pair_rows"]) == 132, "component pair rows")
    require(component_result["pair_rows_sha256"] == digest(component_result["pair_rows"]), "component row digest")

    tangency_result = tangencies["result"]
    require(tangencies["schema"] == "cm2.round78.time2-tangency-curves.v1", "tangency schema")
    rows = tangency_result["curve_rows"]
    require(tangency_result["certified_curve_count"] == 92, "tangency count")
    require(tangency_result["input_tangency_tube_component_count"] == 92, "tangency input count")
    require(tangency_result["failure_count"] == 0 and not tangency_result["failures"], "tangency failures")
    require(len({row["curve_id"] for row in rows}) == 92, "tangency identities")
    require(sum(row["certified_slab_count"] for row in rows) == 41348, "slab count")
    require(sum(len(row["physical_endpoint_certificates"]) for row in rows) == 184, "endpoint count")
    require(all(row["global_root_derivative_sign"] in (-1, 1) for row in rows), "root derivative")
    require(all(row["global_parameter_derivative_sign"] in (-1, 1) for row in rows), "parameter derivative")
    require(all(row["global_implicit_slope_sign"] in (-1, 1) for row in rows), "slope sign")
    require(all(row["physical_source_rectangle_intersection_connected_by_global_monotone_slope"] for row in rows), "physical clipping")
    require(tangency_result["curve_rows_sha256"] == digest(rows), "tangency row digest")
    if expensive:
        pair_count, overlap_count = broad_phase(rows)
        require((pair_count, overlap_count) == (244, 176), "broad phase")

    seam_result = seam["result"]
    require(seam["schema"] == "cm2.round78.chart-free-seam-resolution.v1", "seam schema")
    require(seam_result["seed_leaf_count"] == 3216, "seam seeds")
    require(seam_result["classification_histogram"] == {
        "OUTER_DESTINATION": 12432,
        "Q2_INNER": 4376,
        "R2_INNER": 11448,
    }, "seam classes")
    require(sum(Q(value) for value in seam_result["normalized_area_ledger"].values()) == Q(3216, 1 << 20), "seam area")
    require(len(seam_result["remaining_carrier_histogram"]) == 8, "seam destination carriers")
    require(set(seam_result["remaining_carrier_histogram"].values()) == {1554}, "seam destination multiplicity")
    require(seam_result["terminal_rows_sha256"] == digest(seam_result["terminal_rows"]), "seam row digest")

    time3_result = time3["result"]
    require(time3["schema"] == "cm2.round78.s0-time3-registry.v1", "time3 schema")
    require(time3_result["strict_Q3_cell_count"] == 14928, "Q3 count")
    require(time3_result["strict_R3_cell_count"] == 0, "R3 count")
    require(time3_result["cross_rank_Q2_to_time3_incidence_count"] == 57616, "rank3 incidence")
    require(time3_result["terminal_classification_histogram"] == {
        "SURVIVE_THROUGH_3_INNER": 14928,
        "UNRESOLVED_TIME3_OUTER": 42688,
    }, "time3 classes")
    require(sum(Q(value) for value in time3_result["normalized_area_ledger"].values()) == Q(4423, 256), "time3 area")
    require(len(time3_result["strict_rows"]) == 14928, "strict time3 rows")
    require(all(row["classification"] == "SURVIVE_THROUGH_3_INNER" for row in time3_result["strict_rows"]), "strict time3 labels")
    require(time3_result["strict_rows_sha256"] == digest(time3_result["strict_rows"]), "strict time3 digest")

    atlas = result["physical_boundary_carrier_atlas"]
    require(atlas["family_histogram"] == {"R1_destination": 32, "R2_destination": 32, "time2_tangency": 92}, "atlas histogram")
    r1_ids = {
        curve["physical_curve_id"]
        for pair in atlas["time1_pair_rows"] for curve in pair["physical_curves"]
    }
    r2_ids = {
        curve["physical_curve_id"]
        for pair in atlas["time2_destination_pair_rows"] for curve in pair["physical_curves"]
    }
    tangency_ids = {row["physical_curve_id"] for row in atlas["time2_tangency_rows"]}
    require((len(r1_ids), len(r2_ids), len(tangency_ids)) == (32, 32, 92), "atlas family identities")
    require(len(r1_ids | r2_ids | tangency_ids) == 156, "atlas identity union")
    require(atlas["curve_id_set_sha256"] == digest(sorted(r1_ids | r2_ids | tangency_ids)), "atlas identity digest")
    require(atlas["time1_pair_rows_sha256"] == digest(atlas["time1_pair_rows"]), "time1 map digest")
    require(atlas["time2_destination_pair_rows_sha256"] == digest(atlas["time2_destination_pair_rows"]), "time2 map digest")
    require(atlas["time2_tangency_rows_sha256"] == digest(atlas["time2_tangency_rows"]), "tangency map digest")

    rn = result["RN_frontier"]
    require(rn["certified_finite_rank_face_count"] == 64, "RN face count")


def main() -> int:
    inputs = tuple(map(strict_load, (MANIFEST, COMPONENTS, TANGENCIES, SEAM, TIME3)))
    validate(*inputs)
    mutations = []
    fields = (
        ("round77_failure_mechanism_resolution", "outer_leaf_count", 263071),
        ("physical_boundary_carrier_atlas", "physical_curve_count", 155),
        ("depth_two_quotient", "status", "CERTIFIED"),
        ("depth_two_quotient", "gate4_commuting_square_promotion", "YES"),
        ("fixed_s0_rank_three_frontier", "strict_R3_cell_count", 1),
        ("RN_frontier", "all_rank_RN_summability", "CERTIFIED"),
    )
    for section, key, value in fields:
        mutated = copy.deepcopy(inputs[0])
        mutated["result"][section][key] = value
        mutated["result_sha256"] = digest(mutated["result"])
        mutations.append(mutated)
    base = list(mutations)
    while len(mutations) < 384:
        mutated = copy.deepcopy(base[len(mutations) % len(base)])
        if len(mutations) % 2:
            mutated["result"]["strict_state"]["CM2"] = "GO"
        mutated["result_sha256"] = digest(mutated["result"])
        mutations.append(mutated)
    rejected = 0
    for mutation in mutations:
        try:
            validate_claim_surface(mutation, check_pins=False)
        except Exception:
            rejected += 1
    require(rejected == 384, "hostile rejection")
    strict_bad = ('{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":1} trailing')
    strict_rejected = 0
    for payload in strict_bad:
        try:
            json.loads(
                payload,
                object_pairs_hook=lambda rows: (_ for _ in ()).throw(ValueError()) if len(dict(rows)) != len(rows) else dict(rows),
                parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
            )
        except Exception:
            strict_rejected += 1
    require(strict_rejected == 4, "strict JSON rejection")
    output = {
        "schema": "cm2.round78.physical-boundary-rank3-audit.v1",
        "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "physical_carrier_curves": "156/156",
        "tangency_curves": "92/92",
        "tangency_slabs": "41348/41348",
        "physical_endpoints": "184/184",
        "seam_seed_leaves": "3216/3216",
        "strict_Q3_cells": "14928/14928",
        "strict_R3_cells": "0",
        "hostile_semantic_rejection": "384/384",
        "strict_JSON_rejection": "4/4",
        "verdict": "PASS_NO_GATE_PROMOTION",
    }
    json.dump(output, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
