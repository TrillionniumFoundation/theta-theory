#!/usr/bin/env python3
"""Adaptive interval first-hit atlas for the complete G:E source cell.

The domain covered is the closed rational superset

    t in [-708/1000,708/1000], p in [-1,1], s in [-1/400,1/400].

It contains the actual G:E chart, whose t range is
[-1/sqrt(2),1/sqrt(2)] and whose phase interior has |p|<1.  Every retained
target comes from ``cm2_gate3_candidate_first_hit_cert.py``.

Leaves are classified fail-closed as:

* ``unique_first``: one positive incoming root is strictly earlier than every
  other retained target throughout the box;
* ``tangency_graph``: one physical first tangency is a unique monotone graph
  in p across the box, with all competitors strictly later or absent;
* ``multi_candidate``: the interval evidence does not isolate one of the
  preceding alternatives at the configured depth;
* ``no_future_root``: all retained roots are rigorously absent/behind (this
  should not occur on the physical domain because tau_max<3).

The union of leaves is an exact dyadic partition of the rational superset.
``multi_candidate`` is evidence, not a completed event row.  Therefore this
script does not certify the global Gate-3 inventory, incidence normal forms,
DQ, or scalar-current matching.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as base


ctx.prec = 192
Q = Fraction
CHART_ID = "G:E"
T_LOWER = Q(-708, 1000)
T_UPPER = Q(708, 1000)
P_LOWER = Q(-1)
P_UPPER = Q(1)
S_LOWER = -base.EPS
S_UPPER = base.EPS
INITIAL_T = 8
INITIAL_P = 16
MAX_DEPTH = 8


@dataclass(frozen=True)
class AtlasBox:
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    s0: Q
    s1: Q
    depth: int
    path: str


@dataclass(frozen=True)
class RootRecord:
    target_id: str
    classification: str
    ell: arb
    discriminant: arb
    near: arb | None
    far: arb | None
    transverse: arb


@dataclass(frozen=True)
class Leaf:
    box: AtlasBox
    classification: str
    owner_target: str | None
    active_targets: tuple[str, ...]
    tangency_targets: tuple[str, ...]
    reason: str


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def arb_hull(lower: arb, upper: arb) -> arb:
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    return middle + arb(0, radius.upper())


def sqrt_one_minus_square(lower: Q, upper: Q) -> arb:
    """Dependency-free enclosure of sqrt(1-x^2) on a rational interval."""

    assert Q(-1) <= lower <= upper <= Q(1)
    maximum_abs = max(abs(lower), abs(upper))
    minimum_abs = Q(0) if lower <= 0 <= upper else min(abs(lower), abs(upper))
    value_lower = base.arbq(1 - maximum_abs * maximum_abs).sqrt()
    value_upper = base.arbq(1 - minimum_abs * minimum_abs).sqrt()
    return arb_hull(value_lower.lower(), value_upper.upper())


def geometry(box: AtlasBox) -> tuple[arb, arb, arb, arb, arb, arb]:
    t = base.arb_interval(box.t0, box.t1)
    p = base.arb_interval(box.p0, box.p1)
    s = base.arb_interval(box.s0, box.s1)
    nx = sqrt_one_minus_square(box.t0, box.t1)
    ny = t
    cp = sqrt_one_minus_square(box.p0, box.p1)
    ux = cp * nx - p * ny
    uy = cp * ny + p * nx
    qx = base.arbq(base.RADIUS["G"]) * nx
    qy = base.arbq(base.RADIUS["G"]) * ny
    return qx, qy, ux, uy, s, cp


def root_record_from_geometry(
    geom: tuple[arb, arb, arb, arb, arb, arb], target_id: str
) -> RootRecord:
    qx, qy, ux, uy, s, _cp = geom
    target = base.target_by_id(target_id)
    ax, ay = base.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = base.arbq(base.RADIUS[target.obstacle])
    discriminant = radius * radius - transverse * transverse
    if bool(discriminant < 0):
        return RootRecord(
            target_id, "no_real_intersection", ell, discriminant, None, None, transverse
        )
    if not bool(discriminant > 0):
        return RootRecord(
            target_id, "unresolved_discriminant", ell, discriminant, None, None, transverse
        )
    radical = discriminant.sqrt()
    near, far = ell - radical, ell + radical
    if bool(far < 0):
        classification = "intersection_behind"
    elif bool(near > 0):
        classification = "strict_future_root"
    else:
        classification = "unresolved_root_sign"
    return RootRecord(
        target_id, classification, ell, discriminant, near, far, transverse
    )


CANDIDATE_IDS = tuple(base.candidate_ids(CHART_ID))


def records(box: AtlasBox) -> list[RootRecord]:
    geom = geometry(box)
    return [root_record_from_geometry(geom, target_id) for target_id in CANDIDATE_IDS]


def root_interval_at_fixed_p(box: AtlasBox, target_id: str, p: Q) -> RootRecord:
    face = AtlasBox(box.t0, box.t1, p, p, box.s0, box.s1, box.depth, box.path)
    return root_record_from_geometry(geometry(face), target_id)


def earliest_possible_root_lower(record: RootRecord) -> arb | None:
    """A rigorous lower bound for any real incoming root in the record.

    This remains useful when the discriminant ball straddles zero.  Since
    ``sqrt(Delta) <= sqrt(max(Delta.upper,0))``, every possible near root is
    at least ``ell.lower-sqrt(Delta.upper)``.  The bound can be negative; it
    is used only to prove that an already selected positive root is earlier.
    """

    if record.classification in {"no_real_intersection", "intersection_behind"}:
        return None
    if record.classification == "strict_future_root" and record.near is not None:
        return record.near.lower()
    upper = record.discriminant.upper()
    if not bool(upper > 0):
        return None
    return record.ell.lower() - upper.sqrt().upper()


def physical_tangency_graph(
    box: AtlasBox, candidate: RootRecord, all_records: list[RootRecord]
) -> bool:
    """Certify one first-tangency graph over (t,s), monotone in p."""

    if candidate.classification != "unresolved_discriminant":
        return False
    if box.p0 <= -1 or box.p1 >= 1:
        return False
    _qx, _qy, _ux, _uy, _s, cp = geometry(box)
    if not bool(cp > 0) or not bool(candidate.ell > 0):
        return False
    if not bool(candidate.ell < base.arbq(base.TAU_MAX)):
        return False

    derivative = 2 * candidate.transverse * candidate.ell / cp
    if not (bool(derivative > 0) or bool(derivative < 0)):
        return False
    lower_face = root_interval_at_fixed_p(box, candidate.target_id, box.p0)
    upper_face = root_interval_at_fixed_p(box, candidate.target_id, box.p1)
    lower_delta, upper_delta = lower_face.discriminant, upper_face.discriminant
    if bool(derivative > 0):
        if not (bool(lower_delta < 0) and bool(upper_delta > 0)):
            return False
    else:
        if not (bool(lower_delta > 0) and bool(upper_delta < 0)):
            return False

    # At the tangency the occurrence time is ell.  Every competing target
    # must be absent/behind or have a positive root strictly later than ell.
    for other in all_records:
        if other.target_id == candidate.target_id:
            continue
        if other.classification in {"no_real_intersection", "intersection_behind"}:
            continue
        lower = earliest_possible_root_lower(other)
        if lower is None:
            return False
        if not bool(candidate.ell < lower):
            return False
    return True


def classify_box(box: AtlasBox) -> Leaf:
    all_records = records(box)
    strict = [row for row in all_records if row.classification == "strict_future_root"]
    unresolved = [
        row
        for row in all_records
        if row.classification in {"unresolved_discriminant", "unresolved_root_sign"}
    ]

    if not strict and not unresolved:
        return Leaf(box, "no_future_root", None, (), (), "all roots absent or behind")

    for candidate in strict:
        assert candidate.near is not None
        earlier_than_all = True
        for other in all_records:
            if other.target_id == candidate.target_id:
                continue
            if other.classification in {"no_real_intersection", "intersection_behind"}:
                continue
            lower = earliest_possible_root_lower(other)
            if lower is None or not bool(candidate.near < lower):
                earlier_than_all = False
                break
        if earlier_than_all:
            return Leaf(
                box,
                "unique_first",
                candidate.target_id,
                (candidate.target_id,),
                (),
                "selected incoming root strictly precedes every possible competitor root",
            )

    tangencies = tuple(
        row.target_id
        for row in unresolved
        if physical_tangency_graph(box, row, all_records)
    )
    if len(tangencies) == 1:
        return Leaf(
            box,
            "tangency_graph",
            tangencies[0],
            tangencies,
            tangencies,
            "unique monotone physical first-tangency graph in p",
        )

    # Retain only strict roots not proved later than another strict root, plus
    # every interval-unresolved target.  This is a conservative active set.
    active: set[str] = set()
    for candidate in strict + unresolved:
        lower = earliest_possible_root_lower(candidate)
        if lower is None:
            active.add(candidate.target_id)
            continue
        if not any(
            other.target_id != candidate.target_id
            and other.near is not None
            and bool(other.near < lower)
            for other in strict
        ):
            active.add(candidate.target_id)
    return Leaf(
        box,
        "multi_candidate",
        None,
        tuple(sorted(active)),
        tangencies,
        "interval root ordering or boundary type not isolated",
    )


def split(box: AtlasBox) -> tuple[AtlasBox, AtlasBox]:
    widths = (box.t1 - box.t0, box.p1 - box.p0, box.s1 - box.s0)
    axis = max(range(3), key=lambda index: widths[index])
    depth = box.depth + 1
    if axis == 0:
        middle = (box.t0 + box.t1) / 2
        return (
            AtlasBox(box.t0, middle, box.p0, box.p1, box.s0, box.s1, depth, box.path + "0"),
            AtlasBox(middle, box.t1, box.p0, box.p1, box.s0, box.s1, depth, box.path + "1"),
        )
    if axis == 1:
        middle = (box.p0 + box.p1) / 2
        return (
            AtlasBox(box.t0, box.t1, box.p0, middle, box.s0, box.s1, depth, box.path + "0"),
            AtlasBox(box.t0, box.t1, middle, box.p1, box.s0, box.s1, depth, box.path + "1"),
        )
    middle = (box.s0 + box.s1) / 2
    return (
        AtlasBox(box.t0, box.t1, box.p0, box.p1, box.s0, middle, depth, box.path + "0"),
        AtlasBox(box.t0, box.t1, box.p0, box.p1, middle, box.s1, depth, box.path + "1"),
    )


def initial_boxes() -> list[AtlasBox]:
    boxes = []
    for i in range(INITIAL_T):
        t0 = T_LOWER + (T_UPPER - T_LOWER) * Q(i, INITIAL_T)
        t1 = T_LOWER + (T_UPPER - T_LOWER) * Q(i + 1, INITIAL_T)
        for j in range(INITIAL_P):
            p0 = P_LOWER + (P_UPPER - P_LOWER) * Q(j, INITIAL_P)
            p1 = P_LOWER + (P_UPPER - P_LOWER) * Q(j + 1, INITIAL_P)
            boxes.append(AtlasBox(t0, t1, p0, p1, S_LOWER, S_UPPER, 0, f"{i:02d}.{j:02d}."))
    return boxes


def build_atlas() -> list[Leaf]:
    pending = initial_boxes()
    leaves: list[Leaf] = []
    while pending:
        box = pending.pop()
        leaf = classify_box(box)
        if leaf.classification in {"unique_first", "tangency_graph", "no_future_root"}:
            leaves.append(leaf)
        elif box.depth >= MAX_DEPTH:
            leaves.append(leaf)
        else:
            pending.extend(split(box))
    return sorted(leaves, key=lambda leaf: leaf.box.path)


def box_volume(box: AtlasBox) -> Q:
    return (box.t1 - box.t0) * (box.p1 - box.p0) * (box.s1 - box.s0)


def leaf_row(leaf: Leaf) -> dict[str, Any]:
    box = leaf.box
    return {
        "leaf_id": box.path,
        "box": {
            "t": [str(box.t0), str(box.t1)],
            "p": [str(box.p0), str(box.p1)],
            "s": [str(box.s0), str(box.s1)],
        },
        "depth": box.depth,
        "classification": leaf.classification,
        "owner_target": leaf.owner_target,
        "active_targets": list(leaf.active_targets),
        "tangency_targets": list(leaf.tangency_targets),
        "reason": leaf.reason,
    }


def incidence_rows(leaves: list[Leaf], order: int) -> list[dict[str, Any]]:
    assert order in (2, 3)
    cooccurrence: dict[tuple[str, ...], list[str]] = {}
    for leaf in leaves:
        if leaf.classification != "multi_candidate":
            continue
        for key in itertools.combinations(sorted(leaf.active_targets), order):
            cooccurrence.setdefault(key, []).append(leaf.box.path)
    rows = []
    for key in itertools.combinations(sorted(CANDIDATE_IDS), order):
        witness_ids = cooccurrence.get(key, [])
        rows.append(
            {
                "target_ids": list(key),
                "classification": (
                    "unresolved_cooccurrence_collar"
                    if witness_ids
                    else "separated_by_interval_atlas"
                ),
                "witness_leaf_count": len(witness_ids),
                "witness_leaf_digest": canonical_digest(witness_ids),
            }
        )
    return rows


def summarize(leaves: list[Leaf]) -> dict[str, Any]:
    expected_volume = (T_UPPER - T_LOWER) * (P_UPPER - P_LOWER) * (S_UPPER - S_LOWER)
    actual_volume = sum((box_volume(leaf.box) for leaf in leaves), Q(0))
    assert actual_volume == expected_volume
    counts: dict[str, int] = {}
    volumes: dict[str, Q] = {}
    depth_counts: dict[int, int] = {}
    owners: dict[str, int] = {}
    maximum_active = 0
    full_s_window_leaves = 0
    for leaf in leaves:
        counts[leaf.classification] = counts.get(leaf.classification, 0) + 1
        volumes[leaf.classification] = volumes.get(leaf.classification, Q(0)) + box_volume(leaf.box)
        depth_counts[leaf.box.depth] = depth_counts.get(leaf.box.depth, 0) + 1
        if leaf.box.s0 == S_LOWER and leaf.box.s1 == S_UPPER:
            full_s_window_leaves += 1
        maximum_active = max(maximum_active, len(leaf.active_targets))
        if leaf.owner_target is not None:
            owners[leaf.owner_target] = owners.get(leaf.owner_target, 0) + 1
    rows = [leaf_row(leaf) for leaf in leaves]
    pairs = incidence_rows(leaves, 2)
    triples = incidence_rows(leaves, 3)
    return {
        "chart_id": CHART_ID,
        "domain": {
            "t": [str(T_LOWER), str(T_UPPER)],
            "p": [str(P_LOWER), str(P_UPPER)],
            "s": [str(S_LOWER), str(S_UPPER)],
        },
        "initial_boxes": INITIAL_T * INITIAL_P,
        "max_depth": MAX_DEPTH,
        "leaf_count": len(leaves),
        "classification_counts": counts,
        "classification_volumes": {key: str(value) for key, value in sorted(volumes.items())},
        "depth_counts": {str(key): value for key, value in sorted(depth_counts.items())},
        "owner_counts": owners,
        "maximum_active_targets": maximum_active,
        "full_s_window_leaf_count": full_s_window_leaves,
        "s_split_leaf_count": len(leaves) - full_s_window_leaves,
        "coverage_volume": str(actual_volume),
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


def main() -> None:
    assert len(CANDIDATE_IDS) == 57
    # The rational t interval is a certified closed superset of the true
    # dominant-coordinate cell [-1/sqrt(2),1/sqrt(2)].
    assert T_UPPER == -T_LOWER and T_UPPER * T_UPPER > Q(1, 2)
    leaves = build_atlas()
    summary = summarize(leaves)
    print("GATE3_GE_INTERVAL_ATLAS_COVER: CERTIFIED")
    print(json.dumps(summary, indent=2, sort_keys=True))
    unresolved = summary["classification_counts"].get("multi_candidate", 0)
    if unresolved:
        print("GATE3_GE_EXACT_EVENT_PARTITION: NOT_CERTIFIED")
        print(f"  multi_candidate_leaves={unresolved}")
    else:
        print("GATE3_GE_EXACT_EVENT_PARTITION: CERTIFIED")
    print("GATE3_GLOBAL_DQ_SCALAR_MATCHING: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
