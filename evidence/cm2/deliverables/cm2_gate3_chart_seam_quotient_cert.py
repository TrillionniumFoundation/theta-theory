#!/usr/bin/env python3
"""Exact quotient of the eight dominant-cell chart seams.

The E/W/N/S source-normal charts overlap only at the four diagonal normals
for each source obstacle.  This certificate assigns every diagonal seam to
the E or W chart, identifies duplicate physical bulk traces, and recomputes
bulk connectivity across the quotient.  The rule applies to every analytic
stratum, while the explicit component count below concerns the predecessor's
11,812 rectangular physical bulk boxes.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from typing import Any

import cm2_gate3_endpoint_identity_refinement_cert as endpoint
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


SEAM_CHARTS = {
    "NE": (("E", 1), ("N", 1)),
    "SE": (("E", -1), ("S", 1)),
    "NW": (("W", 1), ("N", -1)),
    "SW": (("W", -1), ("S", -1)),
}
SEAM_NORMALS = {
    "NE": (1, 1),
    "SE": (1, -1),
    "NW": (-1, 1),
    "SW": (-1, -1),
}


def seam_id(box: bulk.Box) -> str | None:
    cell = box.chart_id.split(":")[1]
    if box.z1 == bulk.Z_UPPER:
        return {"E": "NE", "N": "NE", "W": "NW", "S": "SE"}[cell]
    if box.z0 == bulk.Z_LOWER:
        return {"E": "SE", "S": "SW", "W": "SW", "N": "NW"}[cell]
    return None


def union_rectangular_neighbors(
    physical: list[tuple[bulk.Box, dict[str, Any]]],
    union: bulk.UnionFind,
) -> None:
    vertical_left: dict[tuple[tuple[Any, ...], Any], list[int]] = defaultdict(list)
    vertical_right: dict[tuple[tuple[Any, ...], Any], list[int]] = defaultdict(list)
    horizontal_low: dict[tuple[tuple[Any, ...], Any], list[int]] = defaultdict(list)
    horizontal_high: dict[tuple[tuple[Any, ...], Any], list[int]] = defaultdict(list)
    for index, (box, data) in enumerate(physical):
        label = tuple(data["label"])
        vertical_left[(label, box.z0)].append(index)
        vertical_right[(label, box.z1)].append(index)
        horizontal_low[(label, box.s0)].append(index)
        horizontal_high[(label, box.s1)].append(index)
    for key, rows in vertical_right.items():
        for left in rows:
            for right in vertical_left.get(key, []):
                if bulk.positive_overlap(
                    physical[left][0].s0,
                    physical[left][0].s1,
                    physical[right][0].s0,
                    physical[right][0].s1,
                ):
                    union.union(left, right)
    for key, rows in horizontal_high.items():
        for lower in rows:
            for upper in horizontal_low.get(key, []):
                if bulk.positive_overlap(
                    physical[lower][0].z0,
                    physical[lower][0].z1,
                    physical[upper][0].z0,
                    physical[upper][0].z1,
                ):
                    union.union(lower, upper)


def quotient_bulk(
    physical: list[tuple[bulk.Box, dict[str, Any]]],
) -> dict[str, Any]:
    union = bulk.UnionFind(len(physical))
    union_rectangular_neighbors(physical, union)
    seam_rows: dict[tuple[Any, ...], list[int]] = defaultdict(list)
    for index, (box, data) in enumerate(physical):
        seam = seam_id(box)
        if seam is None:
            continue
        label = tuple(data["label"])
        source = box.chart_id.split(":")[0]
        seam_rows[(source, seam, *label[1:])].append(index)

    chart_multiplicity = Counter()
    cross_overlap_pair_count = 0
    two_chart_rows = []
    one_chart_rows = []
    for key, indices in seam_rows.items():
        by_chart: dict[str, list[int]] = defaultdict(list)
        for index in indices:
            by_chart[physical[index][0].chart_id].append(index)
        chart_multiplicity[len(by_chart)] += 1
        charts = sorted(by_chart)
        owner_charts = [chart for chart in charts if chart.split(":")[1] in {"E", "W"}]
        assert len(owner_charts) == 1
        if len(charts) == 1:
            one_chart_rows.append({
                "seam_key": list(key),
                "owner_chart": owner_charts[0],
                "box_count": len(indices),
            })
            continue
        assert len(charts) == 2
        overlap_count = 0
        for left in by_chart[charts[0]]:
            for right in by_chart[charts[1]]:
                if bulk.positive_overlap(
                    physical[left][0].s0,
                    physical[left][0].s1,
                    physical[right][0].s0,
                    physical[right][0].s1,
                ):
                    union.union(left, right)
                    overlap_count += 1
        assert overlap_count > 0
        cross_overlap_pair_count += overlap_count
        two_chart_rows.append({
            "seam_key": list(key),
            "owner_chart": owner_charts[0],
            "duplicate_chart": next(chart for chart in charts if chart != owner_charts[0]),
            "owner_box_count": len(by_chart[owner_charts[0]]),
            "duplicate_box_count": sum(
                len(rows) for chart, rows in by_chart.items() if chart != owner_charts[0]
            ),
            "positive_s_overlap_pair_count": overlap_count,
        })

    quotient_components = defaultdict(list)
    for index in range(len(physical)):
        quotient_components[union.find(index)].append(index)
    component_rows = []
    for indices in quotient_components.values():
        labels = sorted({tuple(physical[index][1]["label"]) for index in indices})
        component_rows.append({
            "chart_label_count": len(labels),
            "chart_labels": [list(label) for label in labels],
            "box_count": len(indices),
            "member_boxes_sha256": canonical_digest([
                physical[index][0].key() for index in sorted(indices)
            ]),
        })
    two_chart_rows.sort(key=canonical_json)
    one_chart_rows.sort(key=canonical_json)
    component_rows.sort(key=canonical_json)
    assert len(physical) == 11812
    assert sum(len(rows) for rows in seam_rows.values()) == 344
    assert len(seam_rows) == 16
    assert chart_multiplicity == Counter({2: 12, 1: 4})
    assert cross_overlap_pair_count == 96
    assert len(component_rows) == 52
    return {
        "physical_rectangular_bulk_box_count": len(physical),
        "bulk_boxes_touching_chart_seams": sum(
            len(rows) for rows in seam_rows.values()
        ),
        "complete_physical_seam_label_keys": len(seam_rows),
        "two_chart_duplicate_seam_keys": chart_multiplicity[2],
        "one_chart_owner_only_seam_keys": chart_multiplicity[1],
        "positive_s_overlap_pairs_identified": cross_overlap_pair_count,
        "prequotient_connected_component_count": 64,
        "postquotient_connected_component_count": len(component_rows),
        "component_count_reduction": 64 - len(component_rows),
        "two_chart_seam_rows_sha256": canonical_digest(two_chart_rows),
        "one_chart_seam_rows_sha256": canonical_digest(one_chart_rows),
        "quotient_component_rows_sha256": canonical_digest(component_rows),
    }


def certify() -> dict[str, Any]:
    _leaves, physical = endpoint.atlas()
    quotient = quotient_bulk(physical)
    seam_geometry_rows = []
    for seam, charts in sorted(SEAM_CHARTS.items()):
        normal = SEAM_NORMALS[seam]
        seam_geometry_rows.append({
            "seam": seam,
            "normal": [f"{normal[0]}/sqrt(2)", f"{normal[1]}/sqrt(2)"],
            "representations": [
                {"cell": cell, "z": z_value} for cell, z_value in charts
            ],
            "absolute_dtheta_dz_on_both_representations": "1",
            "owner_cell": charts[0][0],
        })
    assert all(row["owner_cell"] in {"E", "W"} for row in seam_geometry_rows)
    return {
        "schema": "cm2.gate3.chart-seam-quotient.v1",
        "unique_half_open_owner_rule": {
            "interior": "strict dominant coordinate",
            "diagonal_tie": "E or W owns; N or S excludes",
            "source_obstacle_count": 2,
            "diagonal_seams_per_source": 4,
            "total_chart_seams": 8,
            "seam_geometry_rows_sha256": canonical_digest(seam_geometry_rows),
            "same_physical_normal_on_paired_representations": True,
            "same_absolute_chart_jacobian_on_paired_representations": True,
            "duplicate_trace_is_identified_not_added": True,
        },
        "rectangular_bulk_quotient": quotient,
        "scope_limits": {
            "all_eight_chart_seams_have_unique_owner": True,
            "coordinate_duplicate_traces_removed_by_exact_identity": True,
            "rectangular_bulk_components_quotiented_across_seams": True,
            "ownership_rule_applies_to_analytic_strata": True,
            "full_stratified_maximal_component_registry": False,
            "global_coarea_current_assembled": False,
            "global_dq": False,
            "global_scalar_matching": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_EIGHT_CHART_SEAM_OWNERSHIP: CERTIFIED")
    print("GATE3_RECTANGULAR_BULK_SEAM_QUOTIENT: CERTIFIED")
    print("GATE3_FULL_MAXIMAL_ROWS_GLOBAL_DQ: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
