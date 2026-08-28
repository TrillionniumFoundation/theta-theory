#!/usr/bin/env python3
"""Rigorous bulk atlas of physical Gate-3 tangency subrows.

This certificate works on the exact dominant source-normal cells.  Each cell
is parameterised by ``z in [-1,1]`` with

    t = z/sqrt(2),

so the four E/W/N/S charts meet only on the diagonal seams ``z=+/-1``.
For every parameter-active chart tangency sheet it adaptively partitions the
``(z,s)`` rectangle and proves, box by box, either a strict empty witness or
all of the following physical fields:

* outgoing source carrier and ``0 < ell_T < 3``;
* unique first-visible tangent target;
* unique first non-grazing miss target after the tangent contact;
* a constant nonzero parameter-coarea polarity.

Every positive box is therefore a compact connected immutable *subrow*.
Shared-edge boxes with the same complete label are unioned into certified
connected subrow components.  The construction does not claim that these
components are maximal across the unresolved collars or across chart seams,
and it does not claim global DQ/matching.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as base


ctx.prec = 192
Q = Fraction
SOURCES = ("G", "W")
CELLS = base.CELLS
TARGETS = tuple(base.TARGETS)
TARGET_BY_ID = {target.target_id: target for target in TARGETS}
R = base.RADIUS
S_LOWER, S_UPPER = -base.EPS, base.EPS
Z_LOWER, Z_UPPER = Q(-1), Q(1)
INITIAL_Z = 8
MAX_DEPTH = 9


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def arbq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def arb_interval(lower: Q, upper: Q) -> arb:
    assert lower <= upper
    midpoint = (lower + upper) / 2
    radius = (upper - lower) / 2
    return arb(arbq(midpoint), arbq(radius))


def eta(source: str, target_id: str) -> int:
    return int(TARGET_BY_ID[target_id].obstacle == "W") - int(source == "W")


def active_chart_sheets() -> tuple[tuple[str, str, int], ...]:
    rows = []
    for source in SOURCES:
        for cell in CELLS:
            chart_id = f"{source}:{cell}"
            for target_id in base.candidate_ids(chart_id):
                if eta(source, target_id) == 0:
                    continue
                for epsilon in (-1, 1):
                    rows.append((chart_id, target_id, epsilon))
    rows = tuple(rows)
    assert len(rows) == 384
    return rows


ACTIVE_SHEETS = active_chart_sheets()


# The predecessor proves that the source-wise union of the four chart
# candidate lists is complete for every physical first hit with tau < 3.
# Keeping this finite reduction separate from the all-lift miss check is the
# main performance guard of this certificate: most boxes are rejected before
# the more expensive post-tangency trace is constructed.
GLOBAL_CANDIDATE_IDS = {
    source: tuple(sorted(set().union(*(
        set(base.candidate_ids(f"{source}:{cell}")) for cell in CELLS
    ))))
    for source in SOURCES
}
assert len(GLOBAL_CANDIDATE_IDS["G"]) == 76
assert len(GLOBAL_CANDIDATE_IDS["W"]) == 68

INV_SQRT_TWO = (arb(1) / 2).sqrt()
ARB_RADIUS = {obstacle: arbq(radius) for obstacle, radius in R.items()}
ARB_RADIUS_SQUARED = {
    obstacle: value * value for obstacle, value in ARB_RADIUS.items()
}
TARGET_STATIC = {
    target.target_id: (
        target.obstacle,
        arbq(Q(target.ix) + (Q(1, 2) if target.obstacle == "W" else Q(0))),
        arbq(Q(target.iy) + (Q(1, 2) if target.obstacle == "W" else Q(0))),
    )
    for target in TARGETS
}


def cached_target_center(target_id: str, s: arb) -> tuple[arb, arb]:
    obstacle, x0, y0 = TARGET_STATIC[target_id]
    return x0 + (s if obstacle == "W" else 0), y0


def normal_geometry(
    chart_id: str, z0: Q, z1: Q, s0: Q, s1: Q,
) -> tuple[arb, ...]:
    source, cell = chart_id.split(":")
    z = arb_interval(z0, z1)
    s = arb_interval(s0, s1)
    t = INV_SQRT_TWO * z
    radical = (1 - t * t).sqrt()
    if cell == "E":
        nx, ny = radical, t
    elif cell == "W":
        nx, ny = -radical, t
    elif cell == "N":
        nx, ny = t, radical
    elif cell == "S":
        nx, ny = t, -radical
    else:  # pragma: no cover
        raise ValueError(cell)
    if source == "G":
        cx, cy = arb(0), arb(0)
    else:
        cx, cy = arbq(Q(1, 2)) + s, arbq(Q(1, 2))
    radius = ARB_RADIUS[source]
    qx = cx + radius * nx
    qy = cy + radius * ny
    return nx, ny, qx, qy, s


def tangent_geometry(
    chart_id: str,
    z0: Q,
    z1: Q,
    s0: Q,
    s1: Q,
    target_id: str,
    epsilon: int,
) -> tuple[arb, ...] | None:
    nx, ny, qx, qy, s = normal_geometry(chart_id, z0, z1, s0, s1)
    target = TARGET_BY_ID[target_id]
    ax, ay = cached_target_center(target_id, s)
    dx, dy = ax - qx, ay - qy
    distance_squared = dx * dx + dy * dy
    radius = ARB_RADIUS[target.obstacle]
    radical_squared = distance_squared - radius * radius
    if not bool(radical_squared > 0):
        return None
    ell = radical_squared.sqrt()
    ux = (ell * dx + epsilon * radius * dy) / distance_squared
    uy = (ell * dy - epsilon * radius * dx) / distance_squared
    cp = ux * nx + uy * ny
    p = -ux * ny + uy * nx
    return nx, ny, qx, qy, ux, uy, ell, cp, p, s


def competitor_rows(
    qx: arb,
    qy: arb,
    ux: arb,
    uy: arb,
    s: arb,
    excluded: str,
    target_ids: Iterable[str],
) -> dict[str, tuple[arb, arb, arb]]:
    rows: dict[str, tuple[arb, arb, arb]] = {}
    for target_id in target_ids:
        if target_id == excluded:
            continue
        obstacle, _x0, _y0 = TARGET_STATIC[target_id]
        ax, ay = cached_target_center(target_id, s)
        dx, dy = ax - qx, ay - qy
        ell = ux * dx + uy * dy
        w = -uy * dx + ux * dy
        rows[target_id] = (ell, ARB_RADIUS_SQUARED[obstacle] - w * w, w)
    return rows


@dataclass(frozen=True)
class Box:
    chart_id: str
    target_id: str
    epsilon: int
    z0: Q
    z1: Q
    s0: Q
    s1: Q
    depth: int

    @property
    def area(self) -> Q:
        return (self.z1 - self.z0) * (self.s1 - self.s0)

    def split(self) -> tuple["Box", "Box"]:
        z_relative = (self.z1 - self.z0) / (Z_UPPER - Z_LOWER)
        s_relative = (self.s1 - self.s0) / (S_UPPER - S_LOWER)
        if s_relative > z_relative:
            middle = (self.s0 + self.s1) / 2
            return (
                Box(
                    self.chart_id, self.target_id, self.epsilon,
                    self.z0, self.z1, self.s0, middle, self.depth + 1,
                ),
                Box(
                    self.chart_id, self.target_id, self.epsilon,
                    self.z0, self.z1, middle, self.s1, self.depth + 1,
                ),
            )
        middle = (self.z0 + self.z1) / 2
        return (
            Box(
                self.chart_id, self.target_id, self.epsilon,
                self.z0, middle, self.s0, self.s1, self.depth + 1,
            ),
            Box(
                self.chart_id, self.target_id, self.epsilon,
                middle, self.z1, self.s0, self.s1, self.depth + 1,
            ),
        )

    def key(self) -> dict[str, Any]:
        return {
            "chart_id": self.chart_id,
            "target": self.target_id,
            "epsilon": self.epsilon,
            "z": [str(self.z0), str(self.z1)],
            "s": [str(self.s0), str(self.s1)],
            "depth": self.depth,
        }


def strict_clear_before(
    rows: dict[str, tuple[arb, arb, arb]], threshold: arb,
) -> tuple[bool, str | None]:
    unresolved = False
    for target_id, (ell, delta, _w) in rows.items():
        if bool(delta < 0) or bool(ell < 0) or bool(ell > threshold):
            continue
        if bool(delta > 0) and bool(ell > 0) and bool(ell < threshold):
            return False, target_id
        unresolved = True
    return not unresolved, None


def strict_miss_owner(
    rows: dict[str, tuple[arb, arb, arb]], ell_t: arb,
) -> tuple[str, arb, arb] | None:
    candidates = []
    for target_id, (ell, delta, _w) in rows.items():
        if not (bool(delta > 0) and bool(ell > ell_t)):
            continue
        root = ell - delta.sqrt()
        if not bool(root > ell_t):
            continue
        candidates.append((target_id, ell, delta, root))
    owners = []
    for target_id, ell_m, delta_m, root_m in candidates:
        strict = True
        for other_id, (ell, delta, _w) in rows.items():
            if other_id == target_id:
                continue
            if bool(delta < 0) or bool(ell < ell_t) or bool(ell > ell_m):
                continue
            strict = False
            break
        if strict:
            owners.append((target_id, root_m, delta_m.sqrt()))
    if len(owners) != 1:
        return None
    return owners[0]


def classify_box(box: Box) -> tuple[str, dict[str, Any] | None]:
    geometry = tangent_geometry(
        box.chart_id, box.z0, box.z1, box.s0, box.s1,
        box.target_id, box.epsilon,
    )
    if geometry is None:
        return "unresolved_target_geometry", None
    _nx, _ny, qx, qy, ux, uy, ell_t, cp, p, s = geometry
    if bool(cp < 0):
        return "empty_non_outgoing", None
    if bool(ell_t < 0):
        return "empty_target_behind_source", None
    if bool(ell_t > arbq(base.TAU_MAX)):
        return "empty_target_after_tau3", None
    if bool(p < -1) or bool(p > 1):
        return "empty_source_coordinate", None
    if not (
        bool(cp > 0)
        and bool(ell_t > 0)
        and bool(ell_t < arbq(base.TAU_MAX))
        and bool(p > -1)
        and bool(p < 1)
    ):
        return "unresolved_source_or_target_endpoint", None

    source = box.chart_id.split(":")[0]
    first_rows = competitor_rows(
        qx, qy, ux, uy, s, box.target_id,
        GLOBAL_CANDIDATE_IDS[source],
    )
    clear, blocker = strict_clear_before(first_rows, ell_t)
    if blocker is not None:
        return "empty_target_strictly_occluded", {"blocker": blocker}
    if not clear:
        return "unresolved_first_visibility", None

    all_rows = competitor_rows(
        qx, qy, ux, uy, s, box.target_id,
        (target.target_id for target in TARGETS),
    )
    miss = strict_miss_owner(all_rows, ell_t)
    if miss is None:
        return "unresolved_miss_owner", None
    miss_target, miss_root, miss_incidence = miss

    relative_velocity = eta(box.chart_id.split(":")[0], box.target_id)
    signed_coarea = relative_velocity * box.epsilon * cp * uy / ell_t
    if bool(signed_coarea > 0):
        polarity = 1
    elif bool(signed_coarea < 0):
        polarity = -1
    else:
        return "unresolved_parameter_polarity", None

    return "physical_immutable_subrow", {
        "miss_target": miss_target,
        "polarity": polarity,
        "label": [
            box.chart_id, box.target_id, box.epsilon,
            miss_target, polarity,
        ],
        "target_flight": str(ell_t),
        "source_cosine": str(cp),
        "miss_root": str(miss_root),
        "miss_incidence": str(miss_incidence),
        "signed_coarea": str(signed_coarea),
    }


def initial_boxes() -> Iterable[Box]:
    for chart_id, target_id, epsilon in ACTIVE_SHEETS:
        for index in range(INITIAL_Z):
            z0 = Z_LOWER + (Z_UPPER - Z_LOWER) * Q(index, INITIAL_Z)
            z1 = Z_LOWER + (Z_UPPER - Z_LOWER) * Q(index + 1, INITIAL_Z)
            yield Box(
                chart_id, target_id, epsilon,
                z0, z1, S_LOWER, S_UPPER, 0,
            )


def atlas() -> tuple[list[dict[str, Any]], list[tuple[Box, dict[str, Any]]]]:
    pending = list(initial_boxes())
    leaves: list[dict[str, Any]] = []
    physical: list[tuple[Box, dict[str, Any]]] = []
    while pending:
        box = pending.pop()
        kind, data = classify_box(box)
        if kind.startswith("unresolved_") and box.depth < MAX_DEPTH:
            pending.extend(reversed(box.split()))
            continue
        row = {**box.key(), "classification": kind}
        if data:
            row.update(data)
        leaves.append(row)
        if kind == "physical_immutable_subrow":
            assert data is not None
            physical.append((box, data))
    leaves.sort(key=canonical_json)
    physical.sort(key=lambda row: canonical_json(row[0].key()))
    return leaves, physical


class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        left, right = self.find(left), self.find(right)
        if left != right:
            self.parent[right] = left


def positive_overlap(a0: Q, a1: Q, b0: Q, b1: Q) -> bool:
    return max(a0, b0) < min(a1, b1)


def connected_components(
    physical: list[tuple[Box, dict[str, Any]]],
) -> dict[str, Any]:
    union = UnionFind(len(physical))
    vertical_left: dict[tuple[tuple[Any, ...], Q], list[int]] = defaultdict(list)
    vertical_right: dict[tuple[tuple[Any, ...], Q], list[int]] = defaultdict(list)
    horizontal_low: dict[tuple[tuple[Any, ...], Q], list[int]] = defaultdict(list)
    horizontal_high: dict[tuple[tuple[Any, ...], Q], list[int]] = defaultdict(list)
    for index, (box, data) in enumerate(physical):
        label = tuple(data["label"])
        vertical_left[(label, box.z0)].append(index)
        vertical_right[(label, box.z1)].append(index)
        horizontal_low[(label, box.s0)].append(index)
        horizontal_high[(label, box.s1)].append(index)

    for key, right_rows in vertical_right.items():
        for left in right_rows:
            box_left = physical[left][0]
            for right in vertical_left.get(key, []):
                box_right = physical[right][0]
                if positive_overlap(box_left.s0, box_left.s1, box_right.s0, box_right.s1):
                    union.union(left, right)
    for key, high_rows in horizontal_high.items():
        for lower in high_rows:
            box_lower = physical[lower][0]
            for upper in horizontal_low.get(key, []):
                box_upper = physical[upper][0]
                if positive_overlap(box_lower.z0, box_lower.z1, box_upper.z0, box_upper.z1):
                    union.union(lower, upper)

    members: dict[int, list[int]] = defaultdict(list)
    for index in range(len(physical)):
        members[union.find(index)].append(index)
    rows = []
    for indices in members.values():
        first_box, first_data = physical[indices[0]]
        assert all(physical[index][1]["label"] == first_data["label"] for index in indices)
        area = sum((physical[index][0].area for index in indices), Q(0))
        rows.append({
            "label": first_data["label"],
            "box_count": len(indices),
            "parameter_area": str(area),
            "member_boxes_sha256": canonical_digest([
                physical[index][0].key() for index in indices
            ]),
        })
    rows.sort(key=canonical_json)
    return {
        "certified_connected_subrow_components": len(rows),
        "component_rows_sha256": canonical_digest(rows),
        "largest_component_box_count": max(row["box_count"] for row in rows),
        "component_label_count": len({tuple(row["label"]) for row in rows}),
    }


def reflected_target(source: str, axis: str, target_id: str) -> str:
    target = TARGET_BY_ID[target_id]
    obstacle, ix, iy = target.obstacle, target.ix, target.iy
    if axis == "Jx":
        if source == "G":
            ix = -ix if obstacle == "G" else -ix - 1
        else:
            ix = 1 - ix if obstacle == "G" else -ix
    elif axis == "Jy":
        if source == "G":
            iy = -iy if obstacle == "G" else -iy - 1
        else:
            iy = 1 - iy if obstacle == "G" else -iy
    else:  # pragma: no cover
        raise ValueError(axis)
    return f"{obstacle}[{ix},{iy}]"


def reflected_chart(chart_id: str, axis: str) -> str:
    source, cell = chart_id.split(":")
    if axis == "Jx":
        cell = {"E": "W", "W": "E", "N": "N", "S": "S"}[cell]
    elif axis == "Jy":
        cell = {"E": "E", "W": "W", "N": "S", "S": "N"}[cell]
    else:  # pragma: no cover
        raise ValueError(axis)
    return f"{source}:{cell}"


def reflected_label(label: tuple[Any, ...], axis: str) -> tuple[Any, ...]:
    chart_id, target_id, epsilon, miss_target, polarity = label
    source = chart_id.split(":")[0]
    return (
        reflected_chart(chart_id, axis),
        reflected_target(source, axis, target_id),
        -epsilon,
        reflected_target(source, axis, miss_target),
        -polarity if axis == "Jx" else polarity,
    )


def bulk_symmetry_audit(
    physical: list[tuple[Box, dict[str, Any]]],
) -> dict[str, Any]:
    area_by_label: dict[tuple[Any, ...], Q] = defaultdict(Q)
    count_by_label: Counter[tuple[Any, ...]] = Counter()
    for box, data in physical:
        label = tuple(data["label"])
        area_by_label[label] += box.area
        count_by_label[label] += 1

    labels = set(area_by_label)
    seen: set[tuple[Any, ...]] = set()
    orbits: list[list[list[Any]]] = []
    for label in sorted(labels):
        if label in seen:
            continue
        jx = reflected_label(label, "Jx")
        jy = reflected_label(label, "Jy")
        jxy = reflected_label(jx, "Jy")
        orbit = {label, jx, jy, jxy}
        assert len(orbit) == 4 and orbit <= labels
        areas = {area_by_label[item] for item in orbit}
        counts = {count_by_label[item] for item in orbit}
        assert len(areas) == 1 and len(counts) == 1
        seen.update(orbit)
        orbits.append([list(item) for item in sorted(orbit)])
    assert seen == labels
    signed_parameter_area = sum(
        (Q(label[-1]) * area for label, area in area_by_label.items()), Q(0)
    )
    assert signed_parameter_area == 0
    return {
        "Jx_Jy_label_orbit_count": len(orbits),
        "four_labels_per_orbit": True,
        "box_count_and_parameter_area_equal_within_each_orbit": True,
        "Jx_reverses_parameter_coarea_polarity": True,
        "Jy_preserves_parameter_coarea_polarity": True,
        "paired_bulk_polarity_weighted_parameter_area": str(signed_parameter_area),
        "label_orbits_sha256": canonical_digest(orbits),
        "scope": (
            "exact symmetry matching on the certified bulk only; this is "
            "not the unresolved-collar DQ or physical coarea-current match"
        ),
    }


def certify() -> dict[str, Any]:
    leaves, physical = atlas()
    counts = Counter(row["classification"] for row in leaves)
    area_counts: dict[str, Q] = defaultdict(Q)
    for row in leaves:
        area = (Q(row["z"][1]) - Q(row["z"][0])) * (
            Q(row["s"][1]) - Q(row["s"][0])
        )
        area_counts[row["classification"]] += area
    total_area = len(ACTIVE_SHEETS) * (Z_UPPER - Z_LOWER) * (S_UPPER - S_LOWER)
    assert sum(area_counts.values(), Q(0)) == total_area
    unresolved_area = sum(
        area for kind, area in area_counts.items() if kind.startswith("unresolved_")
    )
    physical_area = area_counts["physical_immutable_subrow"]
    empty_area = total_area - unresolved_area - physical_area
    assert physical_area > 0 and empty_area > 0

    physical_rows = []
    label_counts = Counter()
    for box, data in physical:
        label = tuple(data["label"])
        label_counts[label] += 1
        physical_rows.append({
            **box.key(),
            "miss_target": data["miss_target"],
            "polarity": data["polarity"],
        })

    components = connected_components(physical)
    symmetry = bulk_symmetry_audit(physical)
    result = {
        "schema": "cm2.gate3.global-physical-subrow-atlas.v1",
        "precision_bits": ctx.prec,
        "domain": {
            "dominant_cell_coordinate": "t=z/sqrt(2)",
            "z": [str(Z_LOWER), str(Z_UPPER)],
            "s": [str(S_LOWER), str(S_UPPER)],
            "diagonal_chart_seams": "z=+/-1",
        },
        "active_chart_signed_sheets": len(ACTIVE_SHEETS),
        "initial_z_intervals_per_sheet": INITIAL_Z,
        "maximum_adaptive_depth": MAX_DEPTH,
        "leaf_count": len(leaves),
        "classification_counts": dict(sorted(counts.items())),
        "classification_parameter_areas": {
            key: str(value) for key, value in sorted(area_counts.items())
        },
        "total_parameter_area": str(total_area),
        "certified_physical_parameter_area": str(physical_area),
        "certified_empty_parameter_area": str(empty_area),
        "unresolved_parameter_area": str(unresolved_area),
        "unresolved_area_fraction": str(unresolved_area / total_area),
        "physical_immutable_box_count": len(physical),
        "physical_complete_label_count": len(label_counts),
        "physical_complete_labels_sha256": canonical_digest([
            {"label": list(label), "box_count": count}
            for label, count in sorted(label_counts.items())
        ]),
        "physical_box_rows_sha256": canonical_digest(physical_rows),
        "all_leaf_rows_sha256": canonical_digest(leaves),
        "connected_component_atlas": components,
        "certified_bulk_symmetry_matching": symmetry,
        "scope_limits": {
            "boxes_are_compact_connected_immutable_physical_subrows": True,
            "same_label_shared_edge_unions_are_connected": True,
            "components_maximal_across_unresolved_collars": False,
            "components_quotiented_across_chart_seams": False,
            "global_dq": False,
            "global_scalar_matching": False,
        },
    }
    return result


def main() -> None:
    result = certify()
    print(json.dumps(result, indent=2, sort_keys=True))
    print("GATE3_GLOBAL_BULK_PHYSICAL_SUBROW_ATLAS: CERTIFIED")
    print("GATE3_MAXIMAL_CONNECTED_EVENT_ROWS: NOT_CERTIFIED")
    print("GATE3_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
