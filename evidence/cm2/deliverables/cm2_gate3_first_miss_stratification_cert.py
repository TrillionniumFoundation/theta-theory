#!/usr/bin/env python3
"""Complete active-sheet first-visibility and miss-owner stratification.

The exact owner/Voronoi registry proves that physical first visibility can
change only on a physical earlier common-tangent descriptor and that the
strict next target can change only on a physical later common-tangent
descriptor.  This certificate matches those exhaustive analytic curves to
the depth-thirteen residual boxes of the physical atlas.

Every residual box either meets no physical transition curve and has one
strict midpoint label, or belongs to a strip containing exactly one analytic
curve and has strict, different labels on its two sides.  The resulting
stratification has zero two-dimensional unresolved parameter area.  It does
not assemble maximal connected rows or the global distributional quotient.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_endpoint_identity_refinement_cert as endpoint
import cm2_gate3_global_physical_subrow_atlas_cert as bulk
import cm2_gate3_owner_voronoi_event_registry_cert as owner


ctx.prec = 192
Q = Fraction
HERE = Path(__file__).resolve().parent
FIRST = "unresolved_first_visibility"
MISS = "unresolved_miss_owner"
POLARITY = "unresolved_parameter_polarity"
REFINE_DEPTH = 13
PHYSICAL_KIND = {
    FIRST: "physical_earlier_occlusion_boundary",
    MISS: "physical_later_miss_switch_boundary",
}
OWNER_MANIFEST = HERE / "cm2-gate3-owner-voronoi-event-registry-manifest-2026-07-15.json"
RESOLVER_MANIFEST = HERE / "cm2-gate3-endpoint-descriptor-resolver-manifest-2026-07-15.json"
COLLAR_MANIFEST = HERE / "cm2-gate3-stratified-collar-closure-manifest-2026-07-15.json"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def descriptor_row(descriptor: tuple[str, str, int, str, int, int]) -> dict[str, Any]:
    source, target, epsilon_target, other, epsilon_other, branch = descriptor
    return {
        "source": source,
        "target": target,
        "epsilon_target": epsilon_target,
        "other": other,
        "epsilon_other": epsilon_other,
        "line_branch": branch,
    }


def load_dependency_claims() -> dict[str, Any]:
    owner_data = json.loads(OWNER_MANIFEST.read_text(encoding="utf-8"))
    resolver_data = json.loads(RESOLVER_MANIFEST.read_text(encoding="utf-8"))
    collar_data = json.loads(COLLAR_MANIFEST.read_text(encoding="utf-8"))
    assert owner_data["schema"] == "cm2.gate3.owner-voronoi-event-registry.v1"
    assert owner_data["raw_endpoint_universe"]["target_target_common_tangent_descriptors"] == 82048
    assert owner_data["adaptive_endpoint_completion"]["numerically_unresolved_transition_collar_count"] == 0
    assert owner_data["adaptive_endpoint_completion"]["exact_third_target_tangency_vertices"] == 0
    assert resolver_data["schema"] == "cm2.gate3.endpoint-descriptor-resolver.v1"
    assert resolver_data["verdict"]["empty"] == 320
    assert resolver_data["verdict"]["unresolved"] == 0
    assert resolver_data["verdict"]["physical_joint"] == 0
    assert collar_data["schema"] == "cm2.gate3.stratified-collar-closure.manifest.v1"
    assert collar_data["result"]["residual_first_or_miss_parameter_area"] == "18081/1638400"
    assert collar_data["verdict"]["source_grazing_endpoint_stratification"] == "CERTIFIED"
    assert collar_data["verdict"]["parameter_polarity_stratification"] == "CERTIFIED"
    return {
        "target_target_descriptor_universe": 82048,
        "corrected_unresolved_descriptors_physically_empty": 320,
        "physical_joint_vertices": 0,
        "predecessor_residual_first_or_miss_area": "18081/1638400",
    }


def enumerate_physical_descriptors() -> tuple[
    dict[tuple[str, str, int, str], list[tuple[str, str, int, str, int, int]]],
    dict[str, Any],
]:
    by_key: dict[
        tuple[str, str, int, str],
        list[tuple[str, str, int, str, int, int]],
    ] = defaultdict(list)
    physical_rows = []
    counts = Counter()
    unresolved_count = 0
    for descriptor in owner.common_tangent_descriptors():
        kind = owner.classify_common_tangent_descriptor(*descriptor)
        counts[kind] += 1
        if kind.endswith("_unresolved"):
            unresolved_count += 1
        if kind not in set(PHYSICAL_KIND.values()):
            continue
        source, target, epsilon_target, _other, _epsilon_other, _branch = descriptor
        by_key[(source, target, epsilon_target, kind)].append(descriptor)
        physical_rows.append({**descriptor_row(descriptor), "classification": kind})
    physical_rows.sort(key=canonical_json)
    assert sum(counts.values()) == 82048
    assert counts[PHYSICAL_KIND[FIRST]] == 48
    assert counts[PHYSICAL_KIND[MISS]] == 48
    assert unresolved_count == 288
    return by_key, {
        "strict_full_window_physical_earlier_descriptor_count": 48,
        "strict_full_window_physical_later_descriptor_count": 48,
        "corrected_first_pass_unresolved_descriptor_count": unresolved_count,
        "physical_descriptor_rows_sha256": canonical_digest(physical_rows),
    }


def refined_residual_boxes() -> tuple[list[tuple[bulk.Box, str]], dict[str, Any]]:
    leaves, _physical = endpoint.atlas()
    pending = [
        endpoint.box_from_row(row)
        for row in leaves
        if row["classification"] in {FIRST, MISS}
    ]
    initial_count = len(pending)
    final_counts = Counter()
    final_areas: dict[str, Q] = defaultdict(Q)
    residual = []
    while pending:
        box = pending.pop()
        kind, _data = endpoint.classify_box(box)
        if kind in {FIRST, MISS} and box.depth < REFINE_DEPTH:
            pending.extend(reversed(box.split()))
            continue
        final_counts[kind] += 1
        final_areas[kind] += box.area
        if kind in {FIRST, MISS}:
            residual.append((box, kind))
    residual.sort(key=lambda item: canonical_json({**item[0].key(), "kind": item[1]}))
    assert initial_count == 17912
    assert final_counts[FIRST] == 13216
    assert final_counts[MISS] == 59108
    assert final_areas[FIRST] == Q(413, 204800)
    assert final_areas[MISS] == Q(14777, 1638400)
    assert len(residual) == 72324
    return residual, {
        "initial_depth_nine_first_or_miss_box_count": initial_count,
        "maximum_refinement_depth": REFINE_DEPTH,
        "final_classification_counts": dict(sorted(final_counts.items())),
        "final_classification_ambient_areas": {
            key: str(value) for key, value in sorted(final_areas.items())
        },
        "residual_box_count_before_stratification": len(residual),
        "residual_ambient_box_area_before_stratification": str(
            final_areas[FIRST] + final_areas[MISS]
        ),
    }


def descriptor_z_interval(
    box: bulk.Box,
    descriptor: tuple[str, str, int, str, int, int],
) -> arb | None:
    _status, geometry = owner.common_tangent_source_geometry(
        *descriptor, box.s0, box.s1
    )
    if geometry is None:
        return None
    source_normal_x, source_normal_y = geometry[8], geometry[9]
    cell = box.chart_id.split(":")[1]
    if cell == "E" and bool(source_normal_x < 0):
        return None
    if cell == "W" and bool(source_normal_x > 0):
        return None
    if cell == "N" and bool(source_normal_y < 0):
        return None
    if cell == "S" and bool(source_normal_y > 0):
        return None
    coordinate = (
        source_normal_y if cell in {"E", "W"} else source_normal_x
    )
    z_curve = arb(2).sqrt() * coordinate
    if bool(z_curve < bulk.arbq(box.z0)) or bool(
        z_curve > bulk.arbq(box.z1)
    ):
        return None
    return z_curve


def point_state(
    box: bulk.Box, z_value: Q, s_value: Q, transition_kind: str,
) -> dict[str, Any]:
    point = bulk.Box(
        box.chart_id,
        box.target_id,
        box.epsilon,
        z_value,
        z_value,
        s_value,
        s_value,
        box.depth,
    )
    kind, data = endpoint.classify_box(point)
    assert not kind.startswith("unresolved_")
    if transition_kind == FIRST:
        if kind == "empty_target_strictly_occluded":
            return {"target_visibility": "strictly_occluded"}
        assert kind == "physical_immutable_subrow"
        return {"target_visibility": "physical_first_target"}
    assert transition_kind == MISS
    assert kind == "physical_immutable_subrow" and data is not None
    return {"miss_target": data["miss_target"]}


def state_is_physical(state: dict[str, Any]) -> bool:
    return state.get("target_visibility") == "physical_first_target" or (
        "miss_target" in state
    )


def classify_residual_boxes(
    residual: list[tuple[bulk.Box, str]],
    descriptors: dict[
        tuple[str, str, int, str],
        list[tuple[str, str, int, str, int, int]],
    ],
) -> tuple[dict[str, Any], dict[tuple[Any, ...], list[bulk.Box]]]:
    match_counts = Counter()
    unmatched_counts = Counter()
    matched_counts = Counter()
    unmatched_rows = []
    matched_groups: dict[tuple[Any, ...], list[bulk.Box]] = defaultdict(list)
    active_descriptors = Counter()
    for box, kind in residual:
        source = box.chart_id.split(":")[0]
        candidates = descriptors[
            (source, box.target_id, box.epsilon, PHYSICAL_KIND[kind])
        ]
        matches = []
        for descriptor in candidates:
            z_curve = descriptor_z_interval(box, descriptor)
            if z_curve is not None:
                matches.append(descriptor)
        assert len(matches) <= 1
        match_counts[len(matches)] += 1
        if not matches:
            state = point_state(
                box,
                (box.z0 + box.z1) / 2,
                (box.s0 + box.s1) / 2,
                kind,
            )
            unmatched_counts[kind] += 1
            unmatched_rows.append({**box.key(), "kind": kind, "constant_state": state})
            continue
        descriptor = matches[0]
        matched_counts[kind] += 1
        active_descriptors[descriptor] += 1
        matched_groups[
            (descriptor, box.chart_id, box.s0, box.s1, kind)
        ].append(box)
    unmatched_rows.sort(key=canonical_json)
    assert match_counts == Counter({0: 59028, 1: 13296})
    assert unmatched_counts == Counter({MISS: 50128, FIRST: 8900})
    assert matched_counts == Counter({MISS: 8980, FIRST: 4316})
    assert len(active_descriptors) == 48
    return {
        "boxes_meeting_no_physical_transition_curve": 59028,
        "boxes_meeting_exactly_one_physical_transition_curve": 13296,
        "boxes_meeting_two_or_more_physical_transition_curves": 0,
        "boundary_free_counts_by_kind": dict(sorted(unmatched_counts.items())),
        "one_curve_counts_by_kind": dict(sorted(matched_counts.items())),
        "boundary_free_constant_state_rows_sha256": canonical_digest(unmatched_rows),
        "active_physical_transition_descriptor_count": len(active_descriptors),
        "active_descriptor_box_hit_minimum": min(active_descriptors.values()),
        "active_descriptor_box_hit_maximum": max(active_descriptors.values()),
    }, matched_groups


def stratify_matched_groups(
    matched_groups: dict[tuple[Any, ...], list[bulk.Box]],
) -> dict[str, Any]:
    size_counts = Counter()
    kind_counts = Counter()
    descriptor_groups: dict[tuple[str, str, int, str, int, int], list[dict[str, Any]]] = defaultdict(list)
    group_rows = []
    transition_patterns = Counter()
    for (descriptor, chart_id, s0, s1, kind), boxes in matched_groups.items():
        boxes = sorted(boxes, key=lambda item: (item.z0, item.z1))
        size_counts[len(boxes)] += 1
        kind_counts[kind] += 1
        assert len(boxes) in {1, 2}
        for left, right in zip(boxes, boxes[1:]):
            assert left.z1 >= right.z0
        z0 = min(box.z0 for box in boxes)
        z1 = max(box.z1 for box in boxes)
        envelope = bulk.Box(
            chart_id,
            boxes[0].target_id,
            boxes[0].epsilon,
            z0,
            z1,
            s0,
            s1,
            REFINE_DEPTH,
        )
        z_curve = descriptor_z_interval(envelope, descriptor)
        assert z_curve is not None
        assert bool(z_curve > bulk.arbq(z0)) and bool(z_curve < bulk.arbq(z1))
        s_mid = (s0 + s1) / 2
        lower_state = point_state(envelope, z0, s_mid, kind)
        upper_state = point_state(envelope, z1, s_mid, kind)
        if kind == FIRST:
            assert state_is_physical(lower_state) != state_is_physical(upper_state)
        else:
            assert state_is_physical(lower_state) and state_is_physical(upper_state)
            assert lower_state["miss_target"] != upper_state["miss_target"]
        transition_patterns[(
            kind,
            canonical_json(lower_state),
            canonical_json(upper_state),
        )] += 1
        row = {
            "descriptor": descriptor_row(descriptor),
            "kind": kind,
            "chart_id": chart_id,
            "s": [str(s0), str(s1)],
            "z_envelope": [str(z0), str(z1)],
            "source_box_count": len(boxes),
            "lower_state": lower_state,
            "upper_state": upper_state,
        }
        group_rows.append(row)
        descriptor_groups[descriptor].append(row)

    coverage_rows = []
    descriptor_kind_counts = Counter()
    for descriptor, rows in descriptor_groups.items():
        rows.sort(key=lambda row: (Q(row["s"][0]), Q(row["s"][1]), row["chart_id"]))
        assert len(rows) == 256
        assert Q(rows[0]["s"][0]) == bulk.S_LOWER
        assert Q(rows[-1]["s"][1]) == bulk.S_UPPER
        for left, right in zip(rows, rows[1:]):
            assert Q(left["s"][1]) == Q(right["s"][0])
        kinds = {row["kind"] for row in rows}
        assert len(kinds) == 1
        kind = next(iter(kinds))
        descriptor_kind_counts[kind] += 1
        coverage_rows.append({
            "descriptor": descriptor_row(descriptor),
            "kind": kind,
            "full_parameter_window_covered": True,
            "strip_count": len(rows),
            "strip_rows_sha256": canonical_digest(rows),
        })
    group_rows.sort(key=canonical_json)
    coverage_rows.sort(key=canonical_json)
    assert len(group_rows) == 12288
    assert size_counts == Counter({1: 11280, 2: 1008})
    assert kind_counts == Counter({MISS: 8192, FIRST: 4096})
    assert descriptor_kind_counts == Counter({MISS: 32, FIRST: 16})
    assert sum(transition_patterns.values()) == len(group_rows)
    return {
        "analytic_transition_curve_count": len(descriptor_groups),
        "physical_earlier_transition_curve_count": descriptor_kind_counts[FIRST],
        "physical_later_transition_curve_count": descriptor_kind_counts[MISS],
        "full_window_strips_per_curve": 256,
        "curve_strip_group_count": len(group_rows),
        "source_box_multiplicity_counts": {
            str(key): value for key, value in sorted(size_counts.items())
        },
        "curve_groups_strictly_inside_z_envelopes": len(group_rows),
        "curve_groups_with_strict_distinct_side_states": len(group_rows),
        "transition_pattern_count": len(transition_patterns),
        "transition_patterns_sha256": canonical_digest([
            {
                "kind": key[0],
                "lower_state": json.loads(key[1]),
                "upper_state": json.loads(key[2]),
                "strip_count": value,
            }
            for key, value in sorted(transition_patterns.items())
        ]),
        "curve_strip_rows_sha256": canonical_digest(group_rows),
        "descriptor_full_window_coverage_sha256": canonical_digest(coverage_rows),
    }


def certify() -> dict[str, Any]:
    dependencies = load_dependency_claims()
    descriptors, descriptor_summary = enumerate_physical_descriptors()
    residual, refinement = refined_residual_boxes()
    matching, matched_groups = classify_residual_boxes(residual, descriptors)
    curves = stratify_matched_groups(matched_groups)
    assert matching["active_physical_transition_descriptor_count"] == curves[
        "analytic_transition_curve_count"
    ]
    return {
        "schema": "cm2.gate3.first-miss-stratification.v1",
        "precision_bits": ctx.prec,
        "dependency_claims": dependencies,
        "physical_common_tangent_descriptor_registry": descriptor_summary,
        "depth_thirteen_residual_input": refinement,
        "residual_box_transition_matching": matching,
        "analytic_curve_strip_stratification": curves,
        "remaining_two_dimensional_unresolved_parameter_area": "0",
        "physical_transition_curve_parameter_measure": "0",
        "scope_limits": {
            "active_sheet_first_visibility_stratification_complete": True,
            "active_sheet_miss_owner_stratification_complete": True,
            "all_residual_boxes_have_constant_or_two_sided_strict_labels": True,
            "physical_transition_curves_retained_as_dq_faces": True,
            "maximal_connected_event_rows": False,
            "chart_seams_quotiented": False,
            "global_coarea_current_assembled": False,
            "global_dq": False,
            "global_scalar_matching": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_ACTIVE_FIRST_VISIBILITY_STRATIFICATION: CERTIFIED")
    print("GATE3_ACTIVE_MISS_OWNER_STRATIFICATION: CERTIFIED")
    print("GATE3_TWO_DIMENSIONAL_UNRESOLVED_PARAMETER_AREA: ZERO")
    print("GATE3_MAXIMAL_ROWS_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
