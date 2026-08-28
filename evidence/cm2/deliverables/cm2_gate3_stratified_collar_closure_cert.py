#!/usr/bin/env python3
"""Certified stratification of the Gate-3 source-grazing and polarity collars.

The predecessor atlas stops on boxes that straddle either ``cp=0`` or the
coarea-polarity equation ``u_y=0``.  Those boxes are not two-dimensional
unknown regions.  This certificate keeps the predecessor's strict interval
tests and partitions each source-grazing box into its incoming side, outgoing
side, and analytic boundary.  It likewise partitions every polarity box by
the two signs of ``u_y`` and its analytic zero set.

The remaining first-visibility and miss-owner collars are adaptively refined
from depth nine to depth thirteen.  They remain fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from typing import Any, Iterable

from flint import ctx

import cm2_gate3_endpoint_identity_refinement_cert as endpoint
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


ctx.prec = 192
Q = Fraction
REFINE_DEPTH = 13
ENDPOINT_KIND = "unresolved_genuine_source_grazing_endpoint"
FIRST_KIND = "unresolved_first_visibility"
MISS_KIND = "unresolved_miss_owner"
POLARITY_KIND = "unresolved_parameter_polarity"


def fraction_min_square(constant: Q, slope: Q, radius: Q) -> Q:
    values = (constant - slope * radius, constant + slope * radius)
    if min(values) <= 0 <= max(values):
        return Q(0)
    return min(value * value for value in values)


def affine_center(obstacle: str, ix: int, iy: int) -> tuple[Q, Q, Q]:
    if obstacle == "G":
        return Q(ix), Q(0), Q(iy)
    return Q(ix) + Q(1, 2), Q(1), Q(iy) + Q(1, 2)


def source_center(source: str) -> tuple[Q, Q, Q]:
    if source == "G":
        return Q(0), Q(0), Q(0)
    return Q(1, 2), Q(1), Q(1, 2)


def source_target_separation_registry() -> dict[str, Any]:
    rows = []
    minimum_margin: Q | None = None
    seen = set()
    for chart_id, target_id, _epsilon in bulk.ACTIVE_SHEETS:
        source = chart_id.split(":")[0]
        key = (source, target_id)
        if key in seen:
            continue
        seen.add(key)
        target = bulk.TARGET_BY_ID[target_id]
        assert target.obstacle != source
        tx0, tx1, ty = affine_center(
            target.obstacle, target.ix, target.iy
        )
        sx0, sx1, sy = source_center(source)
        dx0, dx1, dy = tx0 - sx0, tx1 - sx1, ty - sy
        distance_squared_lower = (
            fraction_min_square(dx0, dx1, bulk.base.EPS) + dy * dy
        )
        radius_sum = bulk.R[source] + bulk.R[target.obstacle]
        margin = distance_squared_lower - radius_sum * radius_sum
        assert margin > 0
        minimum_margin = margin if minimum_margin is None else min(
            minimum_margin, margin
        )
        rows.append({
            "source": source,
            "target": target_id,
            "distance_squared_lower": str(distance_squared_lower),
            "radius_sum_squared": str(radius_sum * radius_sum),
            "separation_margin": str(margin),
        })
    rows.sort(key=bulk.canonical_json)
    assert minimum_margin is not None and len(rows) == 64
    return {
        "source_target_pair_count": len(rows),
        "minimum_squared_circle_separation_margin": str(minimum_margin),
        "minimum_squared_angular_derivative_on_cp_zero": str(minimum_margin),
        "minimum_squared_z_derivative_on_cp_zero": str(minimum_margin / 2),
        "registry_sha256": bulk.canonical_digest(rows),
        "identity": (
            "on cp=0, |partial_theta F|^2=|C|^2-"
            "(r_source+sigma*r_target)^2; dominant-cell "
            "|dtheta/dz|^2>=1/2"
        ),
    }


def box_area(row: dict[str, Any]) -> Q:
    return (Q(row["z"][1]) - Q(row["z"][0])) * (
        Q(row["s"][1]) - Q(row["s"][0])
    )


def strict_event_label(
    box: bulk.Box,
) -> tuple[str, dict[str, Any]]:
    geometry = bulk.tangent_geometry(
        box.chart_id,
        box.z0,
        box.z1,
        box.s0,
        box.s1,
        box.target_id,
        box.epsilon,
    )
    assert geometry is not None
    _nx, _ny, qx, qy, ux, uy, ell_t, _cp, _p, s = geometry
    source = box.chart_id.split(":")[0]
    first_rows = bulk.competitor_rows(
        qx,
        qy,
        ux,
        uy,
        s,
        box.target_id,
        bulk.GLOBAL_CANDIDATE_IDS[source],
    )
    clear, blocker = bulk.strict_clear_before(first_rows, ell_t)
    if blocker is not None:
        return "uniformly_occluded", {"blocker": blocker}
    assert clear
    all_rows = bulk.competitor_rows(
        qx,
        qy,
        ux,
        uy,
        s,
        box.target_id,
        (target.target_id for target in bulk.TARGETS),
    )
    miss = bulk.strict_miss_owner(all_rows, ell_t)
    assert miss is not None
    miss_target, _miss_root, _miss_incidence = miss
    polarity_factor = bulk.eta(source, box.target_id) * box.epsilon * uy
    if bool(polarity_factor > 0):
        polarity = 1
    elif bool(polarity_factor < 0):
        polarity = -1
    else:
        raise AssertionError("endpoint-side polarity not strict")
    label = (
        box.chart_id,
        box.target_id,
        box.epsilon,
        miss_target,
        polarity,
    )
    return "physical_outgoing_half", {
        "miss_target": miss_target,
        "polarity": polarity,
        "label": list(label),
    }


def symmetry_orbits(
    label_counts: Counter[tuple[Any, ...]],
    label_areas: dict[tuple[Any, ...], Q],
) -> dict[str, Any]:
    labels = set(label_counts)
    seen = set()
    orbits = []
    for label in sorted(labels):
        if label in seen:
            continue
        orbit = {
            label,
            bulk.reflected_label(label, "Jx"),
            bulk.reflected_label(label, "Jy"),
            bulk.reflected_label(
                bulk.reflected_label(label, "Jx"), "Jy"
            ),
        }
        assert len(orbit) == 4 and orbit <= labels
        assert len({label_counts[item] for item in orbit}) == 1
        assert len({label_areas[item] for item in orbit}) == 1
        seen.update(orbit)
        orbits.append([list(item) for item in sorted(orbit)])
    assert seen == labels
    return {
        "four_label_orbit_count": len(orbits),
        "box_count_and_ambient_area_equal_within_each_orbit": True,
        "orbits_sha256": bulk.canonical_digest(orbits),
    }


def endpoint_stratification(
    leaves: list[dict[str, Any]],
) -> dict[str, Any]:
    endpoint_rows = [
        row for row in leaves if row["classification"] == ENDPOINT_KIND
    ]
    counts = Counter()
    areas: dict[str, Q] = defaultdict(Q)
    label_counts: Counter[tuple[Any, ...]] = Counter()
    label_areas: dict[tuple[Any, ...], Q] = defaultdict(Q)
    rows = []
    predecessor_normal_forms = 0
    for row in endpoint_rows:
        box = endpoint.box_from_row(row)
        if endpoint.common_tangent_normal_form(box) is not None:
            predecessor_normal_forms += 1
        kind, data = strict_event_label(box)
        counts[kind] += 1
        areas[kind] += box.area
        if kind == "physical_outgoing_half":
            label = tuple(data["label"])
            label_counts[label] += 1
            label_areas[label] += box.area
        rows.append({**box.key(), "stratum": kind, **data})
    rows.sort(key=bulk.canonical_json)
    total_area = sum(areas.values(), Q(0))
    assert len(rows) == 23376
    assert total_area == Q(1461, 25600)
    assert predecessor_normal_forms == 16304
    assert counts == Counter({
        "uniformly_occluded": 18980,
        "physical_outgoing_half": 4396,
    })
    assert len(label_counts) == 32
    return {
        "endpoint_box_count": len(rows),
        "ambient_endpoint_collar_area": str(total_area),
        "predecessor_face-certified_normal_form_boxes": predecessor_normal_forms,
        "stratification_counts": dict(sorted(counts.items())),
        "stratification_ambient_box_areas": {
            key: str(value) for key, value in sorted(areas.items())
        },
        "physical_outgoing_half_label_count": len(label_counts),
        "physical_outgoing_half_symmetry": symmetry_orbits(
            label_counts, label_areas
        ),
        "rows_sha256": bulk.canonical_digest(rows),
        "boundary": {
            "equation": "cp=0",
            "globally_regular_on_every_active_source-target sheet": True,
            "two_dimensional_parameter_measure": "0",
            "signed_parameter_coarea_coefficient_on_boundary": "0",
        },
    }


def nonzero_uy_witness(box: bulk.Box) -> dict[str, Any]:
    z_values = (
        (box.z0 + box.z1) / 2,
        box.z0,
        box.z1,
        (3 * box.z0 + box.z1) / 4,
        (box.z0 + 3 * box.z1) / 4,
    )
    s_values = (
        (box.s0 + box.s1) / 2,
        box.s0,
        box.s1,
    )
    for z_value in z_values:
        for s_value in s_values:
            geometry = bulk.tangent_geometry(
                box.chart_id,
                z_value,
                z_value,
                s_value,
                s_value,
                box.target_id,
                box.epsilon,
            )
            if geometry is None:
                continue
            uy = geometry[5]
            if bool(uy > 0):
                return {"z": str(z_value), "s": str(s_value), "sign": 1}
            if bool(uy < 0):
                return {"z": str(z_value), "s": str(s_value), "sign": -1}
    raise AssertionError("failed to prove uy is non-identically zero")


def polarity_partition_row(box: bulk.Box) -> dict[str, Any]:
    geometry = bulk.tangent_geometry(
        box.chart_id,
        box.z0,
        box.z1,
        box.s0,
        box.s1,
        box.target_id,
        box.epsilon,
    )
    assert geometry is not None
    _nx, _ny, qx, qy, ux, uy, ell_t, cp, _p, s = geometry
    assert bool(cp > 0) and bool(ell_t > 0)
    source = box.chart_id.split(":")[0]
    first_rows = bulk.competitor_rows(
        qx,
        qy,
        ux,
        uy,
        s,
        box.target_id,
        bulk.GLOBAL_CANDIDATE_IDS[source],
    )
    clear, blocker = bulk.strict_clear_before(first_rows, ell_t)
    assert clear and blocker is None
    all_rows = bulk.competitor_rows(
        qx,
        qy,
        ux,
        uy,
        s,
        box.target_id,
        (target.target_id for target in bulk.TARGETS),
    )
    miss = bulk.strict_miss_owner(all_rows, ell_t)
    assert miss is not None
    miss_target = miss[0]
    relative_sign = bulk.eta(source, box.target_id) * box.epsilon
    labels = [
        [
            box.chart_id,
            box.target_id,
            box.epsilon,
            miss_target,
            relative_sign * uy_sign,
        ]
        for uy_sign in (-1, 1)
    ]
    return {
        **box.key(),
        "miss_target": miss_target,
        "sign_partition": "uy<0 | uy=0 | uy>0",
        "open_stratum_labels": labels,
        "nonidentity_witness": nonzero_uy_witness(box),
    }


def polarity_stratification(
    boxes: Iterable[bulk.Box],
) -> dict[str, Any]:
    rows = [polarity_partition_row(box) for box in boxes]
    rows.sort(key=bulk.canonical_json)
    area = sum((box_area(row) for row in rows), Q(0))
    base_labels = {
        (
            row["chart_id"], row["target"], row["epsilon"], row["miss_target"]
        )
        for row in rows
    }
    return {
        "box_count": len(rows),
        "ambient_box_area": str(area),
        "base_event_label_count": len(base_labels),
        "open_sign_strata_count_with_multiplicity": 2 * len(rows),
        "all_boxes_have_strict_first_visibility_and_miss_owner": True,
        "all_uy_functions_have_pointwise_nonidentity_witness": True,
        "zero_set_two_dimensional_parameter_measure": "0",
        "rows_sha256": bulk.canonical_digest(rows),
    }


def deep_remaining_refinement(
    leaves: list[dict[str, Any]],
) -> dict[str, Any]:
    pending = [
        endpoint.box_from_row(row)
        for row in leaves
        if row["classification"] in {FIRST_KIND, MISS_KIND}
    ]
    initial_count = len(pending)
    initial_area = sum((box.area for box in pending), Q(0))
    final_rows = []
    polarity_boxes = []
    counts = Counter()
    areas: dict[str, Q] = defaultdict(Q)
    while pending:
        box = pending.pop()
        kind, data = endpoint.classify_box(box)
        if kind in {FIRST_KIND, MISS_KIND} and box.depth < REFINE_DEPTH:
            pending.extend(reversed(box.split()))
            continue
        if kind == POLARITY_KIND:
            polarity_boxes.append(box)
            row = {**box.key(), "classification": "stratified_parameter_polarity"}
        else:
            row = {**box.key(), "classification": kind}
            if data:
                if "miss_target" in data:
                    row["miss_target"] = data["miss_target"]
                if "polarity" in data:
                    row["polarity"] = data["polarity"]
                if "blocker" in data:
                    row["blocker"] = data["blocker"]
        counts[row["classification"]] += 1
        areas[row["classification"]] += box.area
        final_rows.append(row)
    final_rows.sort(key=bulk.canonical_json)
    assert sum(areas.values(), Q(0)) == initial_area
    residual_area = areas[FIRST_KIND] + areas[MISS_KIND]
    polarity = polarity_stratification(polarity_boxes)
    assert polarity["ambient_box_area"] == str(
        areas["stratified_parameter_polarity"]
    )
    return {
        "initial_depth_nine_first_or_miss_box_count": initial_count,
        "initial_depth_nine_first_or_miss_area": str(initial_area),
        "maximum_refinement_depth": REFINE_DEPTH,
        "final_leaf_count": len(final_rows),
        "classification_counts": dict(sorted(counts.items())),
        "classification_ambient_areas": {
            key: str(value) for key, value in sorted(areas.items())
        },
        "residual_first_visibility_area": str(areas[FIRST_KIND]),
        "residual_miss_owner_area": str(areas[MISS_KIND]),
        "residual_first_or_miss_area": str(residual_area),
        "new_polarity_stratification": polarity,
        "rows_sha256": bulk.canonical_digest(final_rows),
    }


def certify() -> dict[str, Any]:
    leaves, _physical = endpoint.atlas()
    counts = Counter(row["classification"] for row in leaves)
    assert counts[ENDPOINT_KIND] == 23376
    assert counts[FIRST_KIND] == 3192
    assert counts[MISS_KIND] == 14720
    assert counts[POLARITY_KIND] == 816
    separation = source_target_separation_registry()
    source_grazing = endpoint_stratification(leaves)
    initial_polarity_boxes = [
        endpoint.box_from_row(row)
        for row in leaves
        if row["classification"] == POLARITY_KIND
    ]
    initial_polarity = polarity_stratification(initial_polarity_boxes)
    remaining = deep_remaining_refinement(leaves)
    predecessor_unresolved = Q(5263, 51200)
    residual = Q(remaining["residual_first_or_miss_area"])
    assert residual < predecessor_unresolved
    return {
        "schema": "cm2.gate3.stratified-collar-closure.v1",
        "precision_bits": ctx.prec,
        "predecessor_unresolved_parameter_area": str(predecessor_unresolved),
        "source_target_separation": separation,
        "source_grazing_endpoint_stratification": source_grazing,
        "initial_parameter_polarity_stratification": initial_polarity,
        "depth_thirteen_remaining_refinement": remaining,
        "residual_first_or_miss_parameter_area": str(residual),
        "residual_fraction_of_full_parameter_domain": str(
            residual / Q(96, 25)
        ),
        "reduction_from_predecessor_unresolved_area": str(
            predecessor_unresolved - residual
        ),
        "fraction_of_predecessor_unresolved_area_removed": str(
            (predecessor_unresolved - residual) / predecessor_unresolved
        ),
        "scope_limits": {
            "all_source_grazing_endpoint_boxes_stratified": True,
            "all_parameter_polarity_boxes_sign_stratified": True,
            "source_grazing_and_polarity_boundaries_are_measure_zero": True,
            "remaining_first_visibility_and_miss_owner_collars_closed": False,
            "maximal_connected_event_rows": False,
            "chart_seams_quotiented": False,
            "global_dq": False,
            "global_scalar_matching": False,
        },
    }


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_SOURCE_GRAZING_COLLAR_STRATIFICATION: CERTIFIED")
    print("GATE3_PARAMETER_POLARITY_STRATIFICATION: CERTIFIED")
    print("GATE3_FIRST_VISIBILITY_MISS_OWNER_CLOSURE: NOT_CERTIFIED")
    print("GATE3_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
