#!/usr/bin/env python3
"""Eight-cell conservative first-hit atlas with exact reflection transport.

This continuation extends the existing complete ``G:E`` cover to the whole
standard collision section.  Four representative charts are evaluated by
192-bit Arb:

    G:E, G:N, W:E, W:N.

The remaining four charts are exact reflected copies.  Vertical reflection
maps E to W and sends ``(p,s)`` to ``(-p,-s)``.  Horizontal reflection maps N
to S and sends ``p`` to ``-p``.  Target lifts are relabelled explicitly.  The
script checks the affine centre-displacement identities and the candidate-list
bijections before transporting any leaf.

Every leaf spans the full physical parameter interval ``|s|<=1/400``.  A
``multi_candidate`` leaf is deliberately unresolved evidence, so this file
does not certify the exact event inventory, DQ, or scalar-current matching.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_ge_interval_atlas_cert as ge


ctx.prec = 192
Q = Fraction
T_LOWER = Q(-177, 250)
T_UPPER = Q(177, 250)
P_LOWER = Q(-1)
P_UPPER = Q(1)
S_LOWER = -base.EPS
S_UPPER = base.EPS
INITIAL_T = 8
INITIAL_P = 16
MAX_DEPTH = 8
REPRESENTATIVES = ("G:E", "G:N", "W:E", "W:N")
ALL_CHARTS = ("G:E", "G:W", "G:N", "G:S", "W:E", "W:W", "W:N", "W:S")

AtlasBox = ge.AtlasBox
RootRecord = ge.RootRecord
Leaf = ge.Leaf


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def geometry(chart_id: str, box: AtlasBox) -> tuple[arb, arb, arb, arb, arb, arb]:
    source, cell = chart_id.split(":")
    t = base.arb_interval(box.t0, box.t1)
    p = base.arb_interval(box.p0, box.p1)
    s = base.arb_interval(box.s0, box.s1)
    radical_n = ge.sqrt_one_minus_square(box.t0, box.t1)
    radical_p = ge.sqrt_one_minus_square(box.p0, box.p1)
    if cell == "E":
        nx, ny = radical_n, t
    elif cell == "W":
        nx, ny = -radical_n, t
    elif cell == "N":
        nx, ny = t, radical_n
    elif cell == "S":
        nx, ny = t, -radical_n
    else:  # pragma: no cover - fixed finite registry
        raise ValueError(cell)
    ux = radical_p * nx - p * ny
    uy = radical_p * ny + p * nx
    if source == "G":
        cx, cy = arb(0), arb(0)
    else:
        cx, cy = base.arbq(Q(1, 2)) + s, base.arbq(Q(1, 2))
    radius = base.arbq(base.RADIUS[source])
    return cx + radius * nx, cy + radius * ny, ux, uy, s, radical_p


def root_record(
    chart_id: str, box: AtlasBox, target_id: str
) -> RootRecord:
    qx, qy, ux, uy, s, _cp = geometry(chart_id, box)
    target = base.target_by_id(target_id)
    ax, ay = base.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = base.arbq(base.RADIUS[target.obstacle])
    discriminant = radius * radius - transverse * transverse
    if bool(discriminant < 0):
        return RootRecord(target_id, "no_real_intersection", ell, discriminant, None, None, transverse)
    if not bool(discriminant > 0):
        return RootRecord(target_id, "unresolved_discriminant", ell, discriminant, None, None, transverse)
    radical = discriminant.sqrt()
    near, far = ell - radical, ell + radical
    if bool(far < 0):
        classification = "intersection_behind"
    elif bool(near > 0):
        classification = "strict_future_root"
    else:
        classification = "unresolved_root_sign"
    return RootRecord(target_id, classification, ell, discriminant, near, far, transverse)


def records(chart_id: str, box: AtlasBox) -> list[RootRecord]:
    return [root_record(chart_id, box, target_id) for target_id in base.candidate_ids(chart_id)]


def root_at_fixed_p(chart_id: str, box: AtlasBox, target_id: str, p: Q) -> RootRecord:
    face = AtlasBox(box.t0, box.t1, p, p, box.s0, box.s1, box.depth, box.path)
    return root_record(chart_id, face, target_id)


def physical_tangency_graph(
    chart_id: str, box: AtlasBox, candidate: RootRecord, all_records: list[RootRecord]
) -> bool:
    if candidate.classification != "unresolved_discriminant":
        return False
    if box.p0 <= -1 or box.p1 >= 1:
        return False
    *_unused, cp = geometry(chart_id, box)
    if not bool(cp > 0) or not bool(candidate.ell > 0) or not bool(candidate.ell < base.arbq(base.TAU_MAX)):
        return False
    derivative = 2 * candidate.transverse * candidate.ell / cp
    if not (bool(derivative > 0) or bool(derivative < 0)):
        return False
    lower = root_at_fixed_p(chart_id, box, candidate.target_id, box.p0).discriminant
    upper = root_at_fixed_p(chart_id, box, candidate.target_id, box.p1).discriminant
    if bool(derivative > 0):
        if not (bool(lower < 0) and bool(upper > 0)):
            return False
    elif not (bool(lower > 0) and bool(upper < 0)):
        return False
    for other in all_records:
        if other.target_id == candidate.target_id:
            continue
        if other.classification in {"no_real_intersection", "intersection_behind"}:
            continue
        lower_root = ge.earliest_possible_root_lower(other)
        if lower_root is None or not bool(candidate.ell < lower_root):
            return False
    return True


def classify_box(chart_id: str, box: AtlasBox) -> Leaf:
    all_records = records(chart_id, box)
    strict = [row for row in all_records if row.classification == "strict_future_root"]
    unresolved = [
        row for row in all_records
        if row.classification in {"unresolved_discriminant", "unresolved_root_sign"}
    ]
    if not strict and not unresolved:
        return Leaf(box, "no_future_root", None, (), (), "all roots absent or behind")
    for candidate in strict:
        assert candidate.near is not None
        if all(
            other.target_id == candidate.target_id
            or other.classification in {"no_real_intersection", "intersection_behind"}
            or (
                (lower := ge.earliest_possible_root_lower(other)) is not None
                and bool(candidate.near < lower)
            )
            for other in all_records
        ):
            return Leaf(
                box, "unique_first", candidate.target_id, (candidate.target_id,), (),
                "selected incoming root strictly precedes every possible competitor root",
            )
    tangencies = tuple(
        row.target_id for row in unresolved
        if physical_tangency_graph(chart_id, box, row, all_records)
    )
    if len(tangencies) == 1:
        return Leaf(
            box, "tangency_graph", tangencies[0], tangencies, tangencies,
            "unique monotone physical first-tangency graph in p",
        )
    active: set[str] = set()
    for candidate in strict + unresolved:
        lower = ge.earliest_possible_root_lower(candidate)
        if lower is None or not any(
            other.target_id != candidate.target_id
            and other.near is not None
            and bool(other.near < lower)
            for other in strict
        ):
            active.add(candidate.target_id)
    return Leaf(
        box, "multi_candidate", None, tuple(sorted(active)), tangencies,
        "interval root ordering or boundary type not isolated",
    )


def initial_boxes() -> list[AtlasBox]:
    boxes: list[AtlasBox] = []
    for i in range(INITIAL_T):
        t0 = T_LOWER + (T_UPPER - T_LOWER) * Q(i, INITIAL_T)
        t1 = T_LOWER + (T_UPPER - T_LOWER) * Q(i + 1, INITIAL_T)
        for j in range(INITIAL_P):
            p0 = P_LOWER + (P_UPPER - P_LOWER) * Q(j, INITIAL_P)
            p1 = P_LOWER + (P_UPPER - P_LOWER) * Q(j + 1, INITIAL_P)
            boxes.append(AtlasBox(t0, t1, p0, p1, S_LOWER, S_UPPER, 0, f"{i:02d}.{j:02d}."))
    return boxes


def build_atlas(chart_id: str) -> list[Leaf]:
    pending = initial_boxes()
    leaves: list[Leaf] = []
    while pending:
        box = pending.pop()
        leaf = classify_box(chart_id, box)
        if leaf.classification in {"unique_first", "tangency_graph", "no_future_root"}:
            leaves.append(leaf)
        elif box.depth >= MAX_DEPTH:
            leaves.append(leaf)
        else:
            pending.extend(ge.split(box))
    return sorted(leaves, key=lambda leaf: leaf.box.path)


def target_parts(target_id: str) -> tuple[str, int, int]:
    target = base.target_by_id(target_id)
    return target.obstacle, target.ix, target.iy


def target_id(obstacle: str, ix: int, iy: int) -> str:
    return f"{obstacle}[{ix},{iy}]"


def reflected_target(source: str, axis: str, value: str) -> str:
    obstacle, ix, iy = target_parts(value)
    if axis == "vertical":
        if source == "G":
            return target_id(obstacle, -ix if obstacle == "G" else -ix - 1, iy)
        return target_id(obstacle, 1 - ix if obstacle == "G" else -ix, iy)
    if axis == "horizontal":
        if source == "G":
            return target_id(obstacle, ix, -iy if obstacle == "G" else -iy - 1)
        return target_id(obstacle, ix, 1 - iy if obstacle == "G" else -iy)
    raise ValueError(axis)


def reflected_chart(chart_id: str, axis: str) -> str:
    source, cell = chart_id.split(":")
    if axis == "vertical" and cell == "E":
        return f"{source}:W"
    if axis == "horizontal" and cell == "N":
        return f"{source}:S"
    raise ValueError((chart_id, axis))


def affine_displacement(source: str, value: str) -> tuple[Q, int, Q, int]:
    """Return dx=a+b*s, dy=c+d*s for target minus source centre."""
    obstacle, ix, iy = target_parts(value)
    if source == "G" and obstacle == "G":
        return Q(ix), 0, Q(iy), 0
    if source == "G" and obstacle == "W":
        return Q(ix) + Q(1, 2), 1, Q(iy) + Q(1, 2), 0
    if source == "W" and obstacle == "G":
        return Q(ix) - Q(1, 2), -1, Q(iy) - Q(1, 2), 0
    return Q(ix), 0, Q(iy), 0


def verify_reflection(chart_id: str, axis: str) -> str:
    source, _cell = chart_id.split(":")
    mapped_chart = reflected_chart(chart_id, axis)
    mapped_ids = [reflected_target(source, axis, value) for value in base.candidate_ids(chart_id)]
    assert len(mapped_ids) == len(set(mapped_ids))
    assert set(mapped_ids) == set(base.candidate_ids(mapped_chart))
    # Check target-minus-source affine displacement exactly.  For V, x is
    # negated and s'=-s; for H, y is negated and s'=s.
    for old, new in zip(base.candidate_ids(chart_id), mapped_ids):
        a, b, c, d = affine_displacement(source, old)
        aa, bb, cc, dd = affine_displacement(source, new)
        if axis == "vertical":
            assert (aa, -bb, cc, -dd) == (-a, -b, c, d)
        else:
            assert (aa, bb, cc, dd) == (a, b, -c, -d)
    return canonical_digest(
        [{"source_target": old, "reflected_target": new} for old, new in zip(base.candidate_ids(chart_id), mapped_ids)]
    )


def reflect_leaf(chart_id: str, axis: str, leaf: Leaf) -> Leaf:
    source, _cell = chart_id.split(":")
    box = leaf.box
    if axis == "vertical":
        mapped_box = AtlasBox(
            box.t0, box.t1, -box.p1, -box.p0, -box.s1, -box.s0,
            box.depth, "V." + box.path,
        )
    else:
        mapped_box = AtlasBox(
            box.t0, box.t1, -box.p1, -box.p0, box.s0, box.s1,
            box.depth, "H." + box.path,
        )
    mapper = lambda value: reflected_target(source, axis, value)
    owner = None if leaf.owner_target is None else mapper(leaf.owner_target)
    return Leaf(
        mapped_box,
        leaf.classification,
        owner,
        tuple(sorted(mapper(value) for value in leaf.active_targets)),
        tuple(sorted(mapper(value) for value in leaf.tangency_targets)),
        f"exact {axis} reflection of {chart_id}: {leaf.reason}",
    )


def box_volume(box: AtlasBox) -> Q:
    return (box.t1 - box.t0) * (box.p1 - box.p0) * (box.s1 - box.s0)


def leaf_row(chart_id: str, leaf: Leaf) -> dict[str, Any]:
    box = leaf.box
    return {
        "chart_id": chart_id,
        "leaf_id": box.path,
        "box": {"t": [str(box.t0), str(box.t1)], "p": [str(box.p0), str(box.p1)], "s": [str(box.s0), str(box.s1)]},
        "depth": box.depth,
        "classification": leaf.classification,
        "owner_target": leaf.owner_target,
        "active_targets": list(leaf.active_targets),
        "tangency_targets": list(leaf.tangency_targets),
        "reason": leaf.reason,
    }


def incidence_rows(candidate_ids: Iterable[str], leaves: list[Leaf], order: int) -> list[dict[str, Any]]:
    cooccurrence: dict[tuple[str, ...], list[str]] = {}
    for leaf in leaves:
        if leaf.classification != "multi_candidate":
            continue
        for key in itertools.combinations(sorted(leaf.active_targets), order):
            cooccurrence.setdefault(key, []).append(leaf.box.path)
    rows = []
    for key in itertools.combinations(sorted(candidate_ids), order):
        witnesses = cooccurrence.get(key, [])
        rows.append({
            "target_ids": list(key),
            "classification": "unresolved_cooccurrence_collar" if witnesses else "separated_by_interval_atlas",
            "witness_leaf_count": len(witnesses),
            "witness_leaf_digest": canonical_digest(witnesses),
        })
    return rows


def summarize(chart_id: str, leaves: list[Leaf], provenance: str) -> dict[str, Any]:
    expected = (T_UPPER - T_LOWER) * (P_UPPER - P_LOWER) * (S_UPPER - S_LOWER)
    assert sum((box_volume(leaf.box) for leaf in leaves), Q(0)) == expected
    counts: dict[str, int] = {}
    volumes: dict[str, Q] = {}
    owners: dict[str, int] = {}
    maximum_active = 0
    for leaf in leaves:
        counts[leaf.classification] = counts.get(leaf.classification, 0) + 1
        volumes[leaf.classification] = volumes.get(leaf.classification, Q(0)) + box_volume(leaf.box)
        maximum_active = max(maximum_active, len(leaf.active_targets))
        if leaf.owner_target is not None:
            owners[leaf.owner_target] = owners.get(leaf.owner_target, 0) + 1
        assert leaf.box.s0 == S_LOWER and leaf.box.s1 == S_UPPER
    pairs = incidence_rows(base.candidate_ids(chart_id), leaves, 2)
    triples = incidence_rows(base.candidate_ids(chart_id), leaves, 3)
    rows = [leaf_row(chart_id, leaf) for leaf in sorted(leaves, key=lambda item: item.box.path)]
    return {
        "chart_id": chart_id,
        "provenance": provenance,
        "candidate_count": len(base.candidate_ids(chart_id)),
        "leaf_count": len(leaves),
        "classification_counts": counts,
        "classification_volumes": {key: str(value) for key, value in sorted(volumes.items())},
        "maximum_active_targets": maximum_active,
        "owner_counts": owners,
        "coverage_volume": str(expected),
        "leaf_rows_sha256": canonical_digest(rows),
        "pair_rows": {
            "count": len(pairs),
            "separated": sum(row["classification"] == "separated_by_interval_atlas" for row in pairs),
            "unresolved": sum(row["classification"] != "separated_by_interval_atlas" for row in pairs),
            "sha256": canonical_digest(pairs),
        },
        "triple_rows": {
            "count": len(triples),
            "separated": sum(row["classification"] == "separated_by_interval_atlas" for row in triples),
            "unresolved": sum(row["classification"] != "separated_by_interval_atlas" for row in triples),
            "sha256": canonical_digest(triples),
        },
    }


def build_all() -> tuple[dict[str, list[Leaf]], dict[str, str]]:
    reflection_digests = {
        "G:E->G:W": verify_reflection("G:E", "vertical"),
        "W:E->W:W": verify_reflection("W:E", "vertical"),
        "G:N->G:S": verify_reflection("G:N", "horizontal"),
        "W:N->W:S": verify_reflection("W:N", "horizontal"),
    }
    atlases = {chart_id: build_atlas(chart_id) for chart_id in REPRESENTATIVES}
    atlases["G:W"] = [reflect_leaf("G:E", "vertical", leaf) for leaf in atlases["G:E"]]
    atlases["W:W"] = [reflect_leaf("W:E", "vertical", leaf) for leaf in atlases["W:E"]]
    atlases["G:S"] = [reflect_leaf("G:N", "horizontal", leaf) for leaf in atlases["G:N"]]
    atlases["W:S"] = [reflect_leaf("W:N", "horizontal", leaf) for leaf in atlases["W:N"]]
    return atlases, reflection_digests


def full_summary() -> dict[str, Any]:
    atlases, reflection_digests = build_all()
    reflected_from = {"G:W": "G:E", "W:W": "W:E", "G:S": "G:N", "W:S": "W:N"}
    summaries = {
        chart_id: summarize(
            chart_id,
            atlases[chart_id],
            "direct_192_bit_Arb" if chart_id in REPRESENTATIVES else f"exact_reflection_of_{reflected_from[chart_id]}",
        )
        for chart_id in ALL_CHARTS
    }
    return {
        "domain": {"t": [str(T_LOWER), str(T_UPPER)], "p": [str(P_LOWER), str(P_UPPER)], "s": [str(S_LOWER), str(S_UPPER)]},
        "maximum_binary_depth": MAX_DEPTH,
        "representative_charts": list(REPRESENTATIVES),
        "reflection_row_digests": reflection_digests,
        "charts": summaries,
        "global_totals": {
            "leaf_count": sum(row["leaf_count"] for row in summaries.values()),
            "unique_first": sum(row["classification_counts"].get("unique_first", 0) for row in summaries.values()),
            "tangency_graph": sum(row["classification_counts"].get("tangency_graph", 0) for row in summaries.values()),
            "multi_candidate": sum(row["classification_counts"].get("multi_candidate", 0) for row in summaries.values()),
            "pair_unresolved": sum(row["pair_rows"]["unresolved"] for row in summaries.values()),
            "triple_unresolved": sum(row["triple_rows"]["unresolved"] for row in summaries.values()),
        },
    }


def main() -> None:
    assert T_UPPER * T_UPPER > Q(1, 2)
    summary = full_summary()
    print("GATE3_EIGHT_CELL_CONSERVATIVE_ATLAS: CERTIFIED")
    print(json.dumps(summary, indent=2, sort_keys=True))
    print("GATE3_EXACT_EVENT_INVENTORY_DQ_SCALAR_MATCHING: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
