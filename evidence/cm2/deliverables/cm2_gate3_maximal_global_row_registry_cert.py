#!/usr/bin/env python3
"""Exact maximal-row registry for every active CM2 tangency sheet.

The predecessor certificates close every two-dimensional ambiguity but stop
before gluing the rectangular and analytic pieces.  This replay works in the
global source-normal circle, so the four dominant-coordinate charts and their
diagonal seams are quotiented from the outset.

For each of the 128 parameter-active signed sheets it enumerates every curve
on which the physical label can change:

* the two source-grazing curves ``cp=0``;
* every forward horizontal-tangent curve ``u_y=0``;
* the 16 active first-visibility curves; and
* the 32 active miss-owner curves.

All candidate curves are analytic over the full parameter window.  Adaptive
Arb separation proves that no two candidates on one sheet intersect.  Their
cyclic order is therefore constant.  A strictly certified witness in every
open angular band fixes its physical state, and adjacent equal states are
merged.  The resulting 64 open bands are connected and maximal because the
enumerated transition universe is exhaustive and every retained boundary has
strictly different side states.

This certificate constructs the geometric occurrence registry.  It does not
claim the global distributional quotient or any CM2 carrier norm.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate3_endpoint_identity_refinement_cert as endpoint
import cm2_gate3_first_miss_stratification_cert as first_miss
import cm2_gate3_global_physical_subrow_atlas_cert as bulk
import cm2_gate3_owner_voronoi_event_registry_cert as owner


ctx.prec = 256
Q = Fraction
HERE = Path(__file__).resolve().parent
S0 = Q(0)
MAX_SEPARATION_DEPTH = 8

FIRST = "physical_earlier_occlusion_boundary"
MISS = "physical_later_miss_switch_boundary"
SOURCE_GRAZING = "source_grazing"
POLARITY = "parameter_polarity"

COLLAR_MANIFEST = (
    HERE / "cm2-gate3-stratified-collar-closure-manifest-2026-07-15.json"
)
FIRST_MISS_MANIFEST = (
    HERE / "cm2-gate3-first-miss-stratification-manifest-2026-07-15.json"
)
SEAM_MANIFEST = (
    HERE / "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def dependency_claims() -> dict[str, Any]:
    collar = json.loads(COLLAR_MANIFEST.read_text(encoding="utf-8"))
    transitions = json.loads(FIRST_MISS_MANIFEST.read_text(encoding="utf-8"))
    seams = json.loads(SEAM_MANIFEST.read_text(encoding="utf-8"))
    assert collar["verdict"]["source_grazing_endpoint_stratification"] == "CERTIFIED"
    assert collar["verdict"]["parameter_polarity_stratification"] == "CERTIFIED"
    assert transitions["verdict"]["active_first_visibility_stratification"] == "CERTIFIED"
    assert transitions["verdict"]["active_miss_owner_stratification"] == "CERTIFIED"
    assert transitions["result"]["remaining_two_dimensional_unresolved_parameter_area"] == "0"
    assert transitions["result"]["dependency_claims"]["physical_joint_vertices"] == 0
    assert seams["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED"
    return {
        "source_grazing_stratification": "CERTIFIED",
        "parameter_polarity_stratification": "CERTIFIED",
        "active_first_visibility_stratification": "CERTIFIED",
        "active_miss_owner_stratification": "CERTIFIED",
        "remaining_two_dimensional_unresolved_parameter_area": "0",
        "physical_target_transition_joint_vertices": 0,
        "eight_chart_seam_ownership": "CERTIFIED",
    }


def active_global_sheets() -> tuple[tuple[str, str, int], ...]:
    rows = []
    for source in bulk.SOURCES:
        for target in bulk.GLOBAL_CANDIDATE_IDS[source]:
            if bulk.eta(source, target) == 0:
                continue
            for epsilon in (-1, 1):
                rows.append((source, target, epsilon))
    rows = tuple(sorted(rows))
    assert len(rows) == 128
    assert len({(source, target) for source, target, _epsilon in rows}) == 64
    return rows


ACTIVE_GLOBAL_SHEETS = active_global_sheets()


def relative_center(
    source: str, target: str, s0: Q, s1: Q,
) -> tuple[arb, arb]:
    s = bulk.arb_interval(s0, s1)
    target_x, target_y = bulk.cached_target_center(target, s)
    if source == "G":
        source_x, source_y = arb(0), arb(0)
    else:
        source_x = bulk.arbq(Q(1, 2)) + s
        source_y = bulk.arbq(Q(1, 2))
    return target_x - source_x, target_y - source_y


def descriptor_tuple(curve: dict[str, Any]) -> tuple[str, str, int, str, int, int]:
    descriptor = curve["descriptor"]
    return (
        descriptor["source"],
        descriptor["target"],
        descriptor["epsilon_target"],
        descriptor["other"],
        descriptor["epsilon_other"],
        descriptor["line_branch"],
    )


def curve_id(curve: dict[str, Any]) -> dict[str, Any]:
    row = {
        "kind": curve["kind"],
        "source": curve["source"],
        "target": curve["target"],
        "epsilon": curve["epsilon"],
    }
    if curve["kind"] == SOURCE_GRAZING:
        row["tangent_direction"] = curve["tangent_direction"]
    elif curve["kind"] == POLARITY:
        row["horizontal_direction"] = curve["horizontal_direction"]
    else:
        row["descriptor"] = curve["descriptor"]
    return row


def curve_key(curve: dict[str, Any]) -> str:
    return canonical_json(curve_id(curve))


def source_grazing_curve(
    source: str, target: str, epsilon: int, tangent_direction: int,
) -> dict[str, Any]:
    return {
        "kind": SOURCE_GRAZING,
        "source": source,
        "target": target,
        "epsilon": epsilon,
        "tangent_direction": tangent_direction,
    }


def polarity_curve(
    source: str, target: str, epsilon: int, horizontal_direction: int,
) -> dict[str, Any]:
    return {
        "kind": POLARITY,
        "source": source,
        "target": target,
        "epsilon": epsilon,
        "horizontal_direction": horizontal_direction,
    }


def transition_curve(kind: str, descriptor: tuple[str, str, int, str, int, int]) -> dict[str, Any]:
    source, target, epsilon, other, epsilon_other, branch = descriptor
    return {
        "kind": kind,
        "source": source,
        "target": target,
        "epsilon": epsilon,
        "descriptor": {
            "source": source,
            "target": target,
            "epsilon_target": epsilon,
            "other": other,
            "epsilon_other": epsilon_other,
            "line_branch": branch,
        },
    }


def curve_normal(
    curve: dict[str, Any], s0: Q, s1: Q,
) -> tuple[arb, arb]:
    source = curve["source"]
    target = curve["target"]
    epsilon = curve["epsilon"]
    center_x, center_y = relative_center(source, target, s0, s1)
    source_radius = bulk.ARB_RADIUS[source]
    target_radius = bulk.ARB_RADIUS[bulk.TARGET_BY_ID[target].obstacle]
    kind = curve["kind"]
    if kind == SOURCE_GRAZING:
        direction = curve["tangent_direction"]
        distance_squared = center_x * center_x + center_y * center_y
        offset = source_radius - direction * epsilon * target_radius
        radical = (distance_squared - offset * offset).sqrt()
        normal_x = (
            offset * center_x + direction * radical * center_y
        ) / distance_squared
        normal_y = (
            offset * center_y - direction * radical * center_x
        ) / distance_squared
        return normal_x, normal_y
    if kind == POLARITY:
        direction = curve["horizontal_direction"]
        normal_y = (
            center_y - direction * epsilon * target_radius
        ) / source_radius
        normal_x = direction * (1 - normal_y * normal_y).sqrt()
        flight = direction * (center_x - source_radius * normal_x)
        assert bool(flight > 0)
        return normal_x, normal_y
    status, geometry = owner.common_tangent_source_geometry(
        *descriptor_tuple(curve), s0, s1
    )
    assert status == "source_intersection" and geometry is not None
    return geometry[8], geometry[9]


def forward_polarity_curve_exists(
    source: str, target: str, epsilon: int, direction: int,
) -> bool:
    center_x, center_y = relative_center(
        source, target, bulk.S_LOWER, bulk.S_UPPER
    )
    source_radius = bulk.ARB_RADIUS[source]
    target_radius = bulk.ARB_RADIUS[bulk.TARGET_BY_ID[target].obstacle]
    normal_y = (
        center_y - direction * epsilon * target_radius
    ) / source_radius
    if not bool(1 - normal_y * normal_y > 0):
        return False
    normal_x = direction * (1 - normal_y * normal_y).sqrt()
    flight = direction * (center_x - source_radius * normal_x)
    return bool(flight > 0)


def active_transition_curves() -> dict[tuple[str, str, int], list[dict[str, Any]]]:
    by_key, _summary = first_miss.enumerate_physical_descriptors()
    rows: dict[tuple[str, str, int], list[dict[str, Any]]] = defaultdict(list)
    counts = Counter()
    for (source, target, epsilon, kind), descriptors in by_key.items():
        if bulk.eta(source, target) == 0:
            continue
        for descriptor in descriptors:
            rows[(source, target, epsilon)].append(
                transition_curve(kind, descriptor)
            )
            counts[kind] += 1
    assert counts == Counter({FIRST: 16, MISS: 32})
    return rows


def candidate_curve_registry() -> tuple[
    dict[tuple[str, str, int], list[dict[str, Any]]], dict[str, Any]
]:
    transitions = active_transition_curves()
    by_sheet: dict[tuple[str, str, int], list[dict[str, Any]]] = {}
    counts = Counter()
    rows = []
    for sheet in ACTIVE_GLOBAL_SHEETS:
        source, target, epsilon = sheet
        curves = [
            source_grazing_curve(source, target, epsilon, direction)
            for direction in (-1, 1)
        ]
        for direction in (-1, 1):
            if forward_polarity_curve_exists(
                source, target, epsilon, direction
            ):
                curves.append(
                    polarity_curve(source, target, epsilon, direction)
                )
        curves.extend(transitions.get(sheet, []))
        curves.sort(key=curve_key)
        assert len({curve_key(curve) for curve in curves}) == len(curves)
        by_sheet[sheet] = curves
        for curve in curves:
            counts[curve["kind"]] += 1
            rows.append(curve_id(curve))
    rows.sort(key=canonical_json)
    assert counts == Counter({
        SOURCE_GRAZING: 256,
        POLARITY: 24,
        FIRST: 16,
        MISS: 32,
    })
    assert len(rows) == 328
    return by_sheet, {
        "active_global_signed_sheet_count": len(ACTIVE_GLOBAL_SHEETS),
        "source_target_pair_count": 64,
        "candidate_curve_count": len(rows),
        "candidate_curve_counts_by_kind": dict(sorted(counts.items())),
        "candidate_curve_rows_sha256": canonical_digest(rows),
    }


def squared_separation(
    left: dict[str, Any], right: dict[str, Any], s0: Q, s1: Q,
) -> arb:
    left_x, left_y = curve_normal(left, s0, s1)
    right_x, right_y = curve_normal(right, s0, s1)
    difference_x = left_x - right_x
    difference_y = left_y - right_y
    return difference_x * difference_x + difference_y * difference_y


def certify_pairwise_separation(
    by_sheet: dict[tuple[str, str, int], list[dict[str, Any]]],
) -> dict[str, Any]:
    pair_count = 0
    full_window_strict = 0
    subdivided_pairs = 0
    maximum_depth = 0
    leaf_rows = []
    for sheet in sorted(by_sheet):
        curves = by_sheet[sheet]
        for right_index, right in enumerate(curves):
            for left in curves[:right_index]:
                pair_count += 1
                pending = [(bulk.S_LOWER, bulk.S_UPPER, 0)]
                pair_leaves = []
                initial_strict = False
                while pending:
                    s0, s1, depth = pending.pop()
                    separation = squared_separation(left, right, s0, s1)
                    if bool(separation > 0):
                        maximum_depth = max(maximum_depth, depth)
                        pair_leaves.append({
                            "s": [str(s0), str(s1)],
                            "depth": depth,
                        })
                        if depth == 0:
                            initial_strict = True
                        continue
                    assert depth < MAX_SEPARATION_DEPTH
                    middle = (s0 + s1) / 2
                    pending.append((middle, s1, depth + 1))
                    pending.append((s0, middle, depth + 1))
                pair_leaves.sort(key=canonical_json)
                if initial_strict:
                    full_window_strict += 1
                else:
                    subdivided_pairs += 1
                leaf_rows.append({
                    "sheet": list(sheet),
                    "left": curve_id(left),
                    "right": curve_id(right),
                    "separation_leaves": pair_leaves,
                })
    leaf_rows.sort(key=canonical_json)
    assert pair_count == 320
    assert full_window_strict == 304
    assert subdivided_pairs == 16
    assert maximum_depth == 1
    assert sum(len(row["separation_leaves"]) for row in leaf_rows) == 336
    return {
        "same_sheet_candidate_pair_count": pair_count,
        "full_window_strict_pair_count": full_window_strict,
        "pairs_requiring_subdivision": subdivided_pairs,
        "maximum_separation_depth": maximum_depth,
        "strict_separation_leaf_count": sum(
            len(row["separation_leaves"]) for row in leaf_rows
        ),
        "all_candidate_curves_pairwise_disjoint": True,
        "cyclic_order_constant_on_full_parameter_window": True,
        "separation_rows_sha256": canonical_digest(leaf_rows),
    }


def cross(left: tuple[arb, arb], right: tuple[arb, arb]) -> arb:
    return left[0] * right[1] - left[1] * right[0]


def choose_anchor(normals: Iterable[tuple[arb, arb]]) -> tuple[int, int]:
    candidates = (
        (1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2),
        (3, 1), (1, 3), (3, 2), (2, 3), (4, 1), (1, 4),
    )
    normals = tuple(normals)
    for anchor in candidates:
        signs = [anchor[0] * normal[1] - anchor[1] * normal[0] for normal in normals]
        if all(bool(value > 0) or bool(value < 0) for value in signs):
            return anchor
    raise AssertionError("failed to find a strict polar-order anchor")


def ordered_curves(
    curves: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[tuple[arb, arb]], tuple[int, int], list[float]]:
    normals_by_key = {
        curve_key(curve): curve_normal(curve, S0, S0) for curve in curves
    }
    anchor = choose_anchor(normals_by_key.values())
    anchor_angle = math.atan2(anchor[1], anchor[0])

    def proposed_angle(curve: dict[str, Any]) -> float:
        normal_x, normal_y = normals_by_key[curve_key(curve)]
        angle = math.atan2(float(normal_y), float(normal_x)) - anchor_angle
        return angle % (2 * math.pi)

    ordered = sorted(curves, key=proposed_angle)
    normals = [normals_by_key[curve_key(curve)] for curve in ordered]
    relative_angles = [proposed_angle(curve) for curve in ordered]
    half = []
    for normal in normals:
        value = anchor[0] * normal[1] - anchor[1] * normal[0]
        assert bool(value > 0) or bool(value < 0)
        half.append(0 if bool(value > 0) else 1)
    assert half == sorted(half)
    for index in range(len(ordered) - 1):
        if half[index] == half[index + 1]:
            assert bool(cross(normals[index], normals[index + 1]) > 0)
    assert all(
        left < right for left, right in zip(relative_angles, relative_angles[1:])
    )
    return ordered, normals, anchor, relative_angles


def witness_normal(theta: float) -> tuple[str, Q, tuple[arb, arb]]:
    normal_x = math.cos(theta)
    normal_y = math.sin(theta)
    if abs(normal_x) >= abs(normal_y):
        cell = "E" if normal_x >= 0 else "W"
        coordinate = normal_y
    else:
        cell = "N" if normal_y >= 0 else "S"
        coordinate = normal_x
    z = Q.from_float(math.sqrt(2) * coordinate).limit_denominator(1 << 42)
    assert bulk.Z_LOWER < z < bulk.Z_UPPER
    geometry = bulk.normal_geometry(f"G:{cell}", z, z, S0, S0)
    return cell, z, (geometry[0], geometry[1])


def band_witness(
    source: str,
    target: str,
    epsilon: int,
    left_normal: tuple[arb, arb],
    right_normal: tuple[arb, arb],
    theta: float,
) -> tuple[dict[str, Any], tuple[Any, ...]]:
    cell, z, sample_normal = witness_normal(theta)
    assert bool(cross(left_normal, sample_normal) > 0)
    assert bool(cross(sample_normal, right_normal) > 0)
    chart_id = f"{source}:{cell}"
    if target not in bulk.base.candidate_ids(chart_id):
        return ({
            "chart_id": chart_id,
            "z": str(z),
            "classification": "empty_chart_candidate_exclusion",
        }, ("empty",))
    box = bulk.Box(chart_id, target, epsilon, z, z, S0, S0, 99)
    kind, data = endpoint.classify_box(box)
    assert not kind.startswith("unresolved_")
    if kind != "physical_immutable_subrow":
        return ({
            "chart_id": chart_id,
            "z": str(z),
            "classification": kind,
        }, ("empty",))
    assert data is not None
    label = (
        source,
        target,
        epsilon,
        data["miss_target"],
        data["polarity"],
    )
    return ({
        "chart_id": chart_id,
        "z": str(z),
        "classification": kind,
        "global_physical_label": list(label),
    }, ("physical", *label))


def boundary_pattern(
    curve: dict[str, Any], left: tuple[Any, ...], right: tuple[Any, ...],
) -> None:
    kind = curve["kind"]
    left_physical = left[0] == "physical"
    right_physical = right[0] == "physical"
    if kind in {SOURCE_GRAZING, FIRST}:
        assert left_physical != right_physical
        return
    assert left_physical and right_physical
    left_label = left[1:]
    right_label = right[1:]
    if kind == MISS:
        assert left_label[:3] == right_label[:3]
        assert left_label[3] != right_label[3]
        assert left_label[4] == right_label[4]
        return
    assert kind == POLARITY
    assert left_label[:4] == right_label[:4]
    assert left_label[4] == -right_label[4]


def enumerate_bands(
    by_sheet: dict[tuple[str, str, int], list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    physical_rows = []
    all_arc_rows = []
    relevant_boundaries = []
    relevant_counts = Counter()
    active_sheet_arc_counts = Counter()
    order_rows = []
    for sheet in sorted(by_sheet):
        source, target, epsilon = sheet
        curves, normals, anchor, angles = ordered_curves(by_sheet[sheet])
        anchor_angle = math.atan2(anchor[1], anchor[0])
        states: list[tuple[Any, ...]] = []
        witnesses = []
        for index, left in enumerate(curves):
            right_index = (index + 1) % len(curves)
            left_angle = angles[index]
            right_angle = angles[right_index]
            if right_index == 0:
                right_angle += 2 * math.pi
            theta = anchor_angle + (left_angle + right_angle) / 2
            witness, state = band_witness(
                source,
                target,
                epsilon,
                normals[index],
                normals[right_index],
                theta,
            )
            states.append(state)
            witnesses.append(witness)
            all_arc_rows.append({
                "sheet": list(sheet),
                "left_boundary": curve_id(left),
                "right_boundary": curve_id(curves[right_index]),
                "witness": witness,
                "state": list(state),
            })

        for index, curve in enumerate(curves):
            left_state = states[index - 1]
            right_state = states[index]
            if left_state == right_state:
                continue
            boundary_pattern(curve, left_state, right_state)
            relevant_counts[curve["kind"]] += 1
            relevant_boundaries.append({
                "curve": curve_id(curve),
                "left_state": list(left_state),
                "right_state": list(right_state),
            })

        starts = [
            index for index, state in enumerate(states)
            if state[0] == "physical" and state != states[index - 1]
        ]
        active_sheet_arc_counts[len(starts)] += 1
        visited = set()
        for start in starts:
            assert start not in visited
            state = states[start]
            arc_indices = [start]
            visited.add(start)
            cursor = (start + 1) % len(states)
            while cursor != start and states[cursor] == state:
                arc_indices.append(cursor)
                visited.add(cursor)
                cursor = (cursor + 1) % len(states)
            label = state[1:]
            row_core = {
                "global_physical_label": list(label),
                "left_boundary": curve_id(curves[start]),
                "right_boundary": curve_id(curves[cursor]),
            }
            physical_rows.append({
                "occurrence_id": "occ:" + canonical_digest(row_core)[:24],
                **row_core,
                "source": source,
                "target": target,
                "epsilon": epsilon,
                "miss_target": label[3],
                "parameter_coarea_polarity": label[4],
                "candidate_arc_piece_count": len(arc_indices),
                "witness": witnesses[start],
                "base": {
                    "parameter_s": [str(bulk.S_LOWER), str(bulk.S_UPPER)],
                    "source_normal": "open cyclic band between analytic boundaries",
                },
            })
        order_rows.append({
            "sheet": list(sheet),
            "anchor": list(anchor),
            "ordered_candidate_boundaries": [curve_id(curve) for curve in curves],
        })

    physical_rows.sort(key=canonical_json)
    all_arc_rows.sort(key=canonical_json)
    relevant_boundaries.sort(key=canonical_json)
    order_rows.sort(key=canonical_json)
    assert relevant_counts == Counter({
        SOURCE_GRAZING: 32,
        FIRST: 16,
        MISS: 32,
        POLARITY: 8,
    })
    assert len(relevant_boundaries) == 88
    assert len(physical_rows) == 64
    labels = [tuple(row["global_physical_label"]) for row in physical_rows]
    assert len(set(labels)) == len(labels)
    assert active_sheet_arc_counts == Counter({0: 104, 1: 8, 2: 4, 3: 4, 4: 4, 5: 4})
    incidence_count = sum(
        1 if row["curve"]["kind"] in {SOURCE_GRAZING, FIRST} else 2
        for row in relevant_boundaries
    )
    assert incidence_count == 2 * len(physical_rows) == 128
    registry = {
        "maximal_connected_physical_row_count": len(physical_rows),
        "active_sheet_count_by_physical_row_multiplicity": {
            str(key): value for key, value in sorted(active_sheet_arc_counts.items())
        },
        "unique_complete_global_physical_label_count": len(set(labels)),
        "physical_row_endpoint_incidence_count": incidence_count,
        "every_row_has_two_boundary_incidences": True,
        "every_row_is_a_connected_open_band_over_full_parameter_window": True,
        "every_retained_boundary_has_strict_distinct_side_states": True,
        "adjacent_equal_states_merged": True,
        "rows_are_maximal_in_exhaustive_transition_arrangement": True,
        "maximal_row_rows_sha256": canonical_digest(physical_rows),
    }
    boundary_registry = {
        "state_changing_boundary_count": len(relevant_boundaries),
        "state_changing_counts_by_kind": dict(sorted(relevant_counts.items())),
        "physical_row_endpoint_incidence_count": incidence_count,
        "candidate_open_arc_count": len(all_arc_rows),
        "cyclic_order_rows_sha256": canonical_digest(order_rows),
        "open_arc_state_rows_sha256": canonical_digest(all_arc_rows),
        "state_changing_boundary_rows_sha256": canonical_digest(relevant_boundaries),
    }
    return physical_rows, registry, boundary_registry


def reflected_global_label(
    label: tuple[str, str, int, str, int], axis: str,
) -> tuple[str, str, int, str, int]:
    source, target, epsilon, miss_target, polarity = label
    return (
        source,
        bulk.reflected_target(source, axis, target),
        -epsilon,
        bulk.reflected_target(source, axis, miss_target),
        -polarity if axis == "Jx" else polarity,
    )


def symmetry_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    labels = {tuple(row["global_physical_label"]) for row in rows}
    seen = set()
    orbits = []
    for label in sorted(labels):
        if label in seen:
            continue
        reflected_x = reflected_global_label(label, "Jx")
        reflected_y = reflected_global_label(label, "Jy")
        reflected_xy = reflected_global_label(reflected_x, "Jy")
        orbit = {label, reflected_x, reflected_y, reflected_xy}
        assert len(orbit) == 4 and orbit <= labels
        seen.update(orbit)
        orbits.append([list(item) for item in sorted(orbit)])
    assert seen == labels
    assert len(orbits) == 16
    return {
        "Jx_Jy_four_row_orbit_count": len(orbits),
        "four_rows_per_orbit": True,
        "Jx_reverses_parameter_coarea_polarity": True,
        "Jy_preserves_parameter_coarea_polarity": True,
        "exact_Jx_row_pair_count": len(rows) // 2,
        "row_orbits_sha256": canonical_digest(orbits),
    }


def certify() -> dict[str, Any]:
    dependencies = dependency_claims()
    curves_by_sheet, candidate_registry = candidate_curve_registry()
    separation = certify_pairwise_separation(curves_by_sheet)
    rows, maximal_registry, boundary_registry = enumerate_bands(curves_by_sheet)
    symmetry = symmetry_audit(rows)
    return {
        "schema": "cm2.gate3.maximal-global-row-registry.v1",
        "precision_bits": ctx.prec,
        "domain": {
            "source_normal_base": "global unit circle; chart seams quotiented",
            "parameter_s": [str(bulk.S_LOWER), str(bulk.S_UPPER)],
            "active_global_signed_sheets": len(ACTIVE_GLOBAL_SHEETS),
        },
        "dependency_claims": dependencies,
        "candidate_transition_registry": candidate_registry,
        "pairwise_curve_separation": separation,
        "state_changing_boundary_registry": boundary_registry,
        "maximal_row_registry": maximal_registry,
        "maximal_row_symmetry": symmetry,
        "scope_limits": {
            "all_active_transition_curves_enumerated": True,
            "all_candidate_curves_pairwise_disjoint_on_each_sheet": True,
            "all_open_bands_have_strict_constant_physical_state": True,
            "chart_seams_quotiented_in_global_normal_circle": True,
            "maximal_connected_event_rows": True,
            "complete_hit_miss_polarity_labels": True,
            "global_coarea_current_assembled": False,
            "arbitrary_test_distributional_quotient": False,
            "global_scalar_matching": False,
            "gate3_certified": False,
            "gate4_certified": False,
            "gate5_certified": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_MAXIMAL_CONNECTED_EVENT_ROWS: CERTIFIED")
    print("GATE3_GLOBAL_CHART_QUOTIENTED_ROW_REGISTRY: CERTIFIED")
    print("GATE3_GLOBAL_COAREA_DQ: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
