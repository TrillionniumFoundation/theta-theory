#!/usr/bin/env python3
"""Gate-3 candidate-target reduction and local first-hit certificates.

This certificate starts from the already certified uniform bound ``tau < 3``
for the standard collision section of the rational two-disk pilot.  It does
two finite, reproducible jobs.

1.  Every one of the 8 source cells and 162 conservative target lifts is
    classified as ``self_source``, ``empty_horizon_center_distance``,
    ``empty_outgoing_halfspace``, or ``retained_candidate``.  All exclusions
    use exact rational inequalities.  The retained lists are conservative:
    no physical first collision before time 3 is discarded.
2.  A generic 256-bit Arb line--circle root engine is exercised on explicit
    open boxes in the G:E and W:E charts.  It proves that G[1,0] and W[1,0],
    respectively, are strict physical first hits throughout those boxes,
    after comparison with every retained competitor.

The script does *not* certify all retained candidate rows, all tangency faces,
pair/triple incidences, or the global DQ/scalar-current assembly.  Gate 3
therefore remains fail-closed.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx


ctx.prec = 256

Q = Fraction
RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}
EPS = Q(1, 400)
TAU_MAX = Q(3)
LIFT_MIN = -4
LIFT_MAX = 4
CELLS = ("E", "W", "N", "S")

# Exact rational brackets for 1/sqrt(2).  They are used only for a safe
# upper support bound on one dominant-coordinate normal cell.
INV_SQRT2_LOWER = Q(707, 1000)
INV_SQRT2_UPPER = Q(708, 1000)


@dataclass(frozen=True)
class Target:
    obstacle: str
    ix: int
    iy: int

    @property
    def target_id(self) -> str:
        return f"{self.obstacle}[{self.ix},{self.iy}]"


@dataclass(frozen=True)
class PhaseBox:
    chart_id: str
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    s0: Q
    s1: Q


def arbq(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def arb_interval(lower: Q, upper: Q) -> arb:
    assert lower <= upper
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    return arbq(middle) + arb(0, arbq(radius).upper())


def targets() -> list[Target]:
    return [
        Target(obstacle, ix, iy)
        for obstacle in ("G", "W")
        for ix in range(LIFT_MIN, LIFT_MAX + 1)
        for iy in range(LIFT_MIN, LIFT_MAX + 1)
    ]


TARGETS = targets()


def vector_interval(
    source: str, target: Target
) -> tuple[Q, Q, Q, Q]:
    """Bounds for target-center minus source-center over |s|<=1/400."""

    ix, iy = target.ix, target.iy
    if source == "G" and target.obstacle == "G":
        return Q(ix), Q(ix), Q(iy), Q(iy)
    if source == "G" and target.obstacle == "W":
        x = Q(2 * ix + 1, 2)
        return x - EPS, x + EPS, Q(2 * iy + 1, 2), Q(2 * iy + 1, 2)
    if source == "W" and target.obstacle == "G":
        x = Q(2 * ix - 1, 2)
        return x - EPS, x + EPS, Q(2 * iy - 1, 2), Q(2 * iy - 1, 2)
    return Q(ix), Q(ix), Q(iy), Q(iy)


def square_min_abs(lower: Q, upper: Q) -> Q:
    if lower <= 0 <= upper:
        return Q(0)
    return min(lower * lower, upper * upper)


def minimum_center_distance_squared(source: str, target: Target) -> Q:
    x0, x1, y0, y1 = vector_interval(source, target)
    return square_min_abs(x0, x1) + square_min_abs(y0, y1)


def absmax(lower: Q, upper: Q) -> Q:
    return max(abs(lower), abs(upper))


def dominant_cell_support_upper(
    cell: str, x0: Q, x1: Q, y0: Q, y1: Q
) -> Q:
    """A rational upper bound for sup v.n over a normal cell and s.

    Write a cell normal as ``n=e cos(alpha)+e_perp sin(alpha)`` with
    ``|alpha|<=pi/4``.  If A=v.e is nonnegative, use
    ``A cos(alpha)<=A``.  If A is negative, use
    ``A cos(alpha)<=A*(707/1000)``.  In both cases use
    ``|B sin(alpha)|<=|B|*(708/1000)``.  Endpoint bounds on the affine
    parameter interval then give the returned rational number.
    """

    if cell == "E":
        a_upper, b_abs = x1, absmax(y0, y1)
    elif cell == "W":
        a_upper, b_abs = -x0, absmax(y0, y1)
    elif cell == "N":
        a_upper, b_abs = y1, absmax(x0, x1)
    elif cell == "S":
        a_upper, b_abs = -y0, absmax(x0, x1)
    else:
        raise ValueError(cell)
    if a_upper >= 0:
        return a_upper + b_abs * INV_SQRT2_UPPER
    return a_upper * INV_SQRT2_LOWER + b_abs * INV_SQRT2_UPPER


def classify(source: str, cell: str, target: Target) -> tuple[str, str]:
    """Return a fail-closed exact classification and its witness inequality."""

    if target.obstacle == source and target.ix == 0 and target.iy == 0:
        return (
            "self_source",
            "same strictly convex source lift; outgoing interior rays do not re-enter it",
        )

    source_radius = RADIUS[source]
    target_radius = RADIUS[target.obstacle]
    horizon_center_threshold = TAU_MAX + source_radius + target_radius
    distance_squared = minimum_center_distance_squared(source, target)
    if distance_squared >= horizon_center_threshold * horizon_center_threshold:
        return (
            "empty_horizon_center_distance",
            f"min_center_distance^2={distance_squared} >= "
            f"(3+R_source+R_target)^2={horizon_center_threshold*horizon_center_threshold}",
        )

    vector = vector_interval(source, target)
    support_upper = dominant_cell_support_upper(cell, *vector)
    outgoing_threshold = source_radius - target_radius
    if support_upper < outgoing_threshold:
        return (
            "empty_outgoing_halfspace",
            f"support_upper={support_upper} < R_source-R_target={outgoing_threshold}",
        )

    return (
        "retained_candidate",
        "not excluded by certified horizon and outgoing-halfspace necessary conditions",
    )


def candidate_ids(chart_id: str) -> list[str]:
    source, cell = chart_id.split(":")
    return [
        target.target_id
        for target in TARGETS
        if classify(source, cell, target)[0] == "retained_candidate"
    ]


def classification_rows(chart_id: str) -> list[dict[str, str]]:
    source, cell = chart_id.split(":")
    rows = []
    for target in TARGETS:
        classification, proof = classify(source, cell, target)
        rows.append(
            {
                "target_id": target.target_id,
                "classification": classification,
                "proof": proof,
            }
        )
    return rows


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def target_by_id(target_id: str) -> Target:
    for target in TARGETS:
        if target.target_id == target_id:
            return target
    raise KeyError(target_id)


def phase_geometry(box: PhaseBox) -> tuple[arb, arb, arb, arb, arb]:
    source, cell = box.chart_id.split(":")
    t = arb_interval(box.t0, box.t1)
    p = arb_interval(box.p0, box.p1)
    s = arb_interval(box.s0, box.s1)
    radical_n = (1 - t * t).sqrt()
    radical_p = (1 - p * p).sqrt()

    if cell == "E":
        nx, ny = radical_n, t
    elif cell == "W":
        nx, ny = -radical_n, t
    elif cell == "N":
        nx, ny = t, radical_n
    elif cell == "S":
        nx, ny = t, -radical_n
    else:
        raise ValueError(cell)

    # Counterclockwise unit tangent n_perp=(-ny,nx).
    ux = radical_p * nx - p * ny
    uy = radical_p * ny + p * nx
    if source == "G":
        cx, cy = arb(0), arb(0)
    else:
        cx, cy = arbq(Q(1, 2)) + s, arbq(Q(1, 2))
    qx = cx + arbq(RADIUS[source]) * nx
    qy = cy + arbq(RADIUS[source]) * ny
    return qx, qy, ux, uy, s


def target_center(target: Target, s: arb) -> tuple[arb, arb]:
    if target.obstacle == "G":
        return arb(target.ix), arb(target.iy)
    return (
        arb(target.ix) + arbq(Q(1, 2)) + s,
        arb(target.iy) + arbq(Q(1, 2)),
    )


def root_data(box: PhaseBox, target: Target) -> dict[str, arb | str]:
    qx, qy, ux, uy, s = phase_geometry(box)
    ax, ay = target_center(target, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    # Multiplication is used explicitly because python-flint 0.9.0's generic
    # power path may return ``nan`` for a ball containing zero.
    target_radius = arbq(RADIUS[target.obstacle])
    discriminant = target_radius * target_radius - transverse * transverse
    result: dict[str, arb | str] = {
        "ell": ell,
        "discriminant": discriminant,
    }
    if bool(discriminant < 0):
        result["classification"] = "no_real_intersection"
        return result
    if not bool(discriminant > 0):
        result["classification"] = "unresolved_discriminant"
        return result
    square_root = discriminant.sqrt()
    near = ell - square_root
    far = ell + square_root
    result["near"] = near
    result["far"] = far
    if bool(far < 0):
        result["classification"] = "intersection_strictly_behind"
    elif bool(near > 0):
        result["classification"] = "strict_future_near_root"
    else:
        result["classification"] = "unresolved_root_sign"
    return result


def certify_first_hit_patch(
    box: PhaseBox, selected_target_id: str
) -> tuple[arb, int, int]:
    selected = target_by_id(selected_target_id)
    selected_data = root_data(box, selected)
    assert selected_data["classification"] == "strict_future_near_root"
    selected_root = selected_data["near"]
    assert isinstance(selected_root, arb)
    assert bool(selected_root < arbq(TAU_MAX))

    missed = 0
    later = 0
    for competitor_id in candidate_ids(box.chart_id):
        if competitor_id == selected_target_id:
            continue
        competitor_data = root_data(box, target_by_id(competitor_id))
        classification = competitor_data["classification"]
        if classification in {"no_real_intersection", "intersection_strictly_behind"}:
            missed += 1
            continue
        if classification != "strict_future_near_root":
            raise RuntimeError(
                f"unresolved competitor {box.chart_id}:{competitor_id}: "
                f"{classification}; data={competitor_data}"
            )
        competitor_root = competitor_data["near"]
        assert isinstance(competitor_root, arb)
        if not bool(selected_root < competitor_root):
            raise RuntimeError(
                f"first-hit comparison unresolved for {box.chart_id}: "
                f"{selected_target_id} vs {competitor_id}; "
                f"selected={selected_root}, competitor={competitor_root}"
            )
        later += 1
    return selected_root, missed, later


def verify_candidate_table() -> dict[str, dict[str, int]]:
    # Exact bracket proof for 1/sqrt(2).
    assert INV_SQRT2_LOWER**2 < Q(1, 2)
    assert INV_SQRT2_UPPER**2 > Q(1, 2)
    assert len(TARGETS) == 162

    counts: dict[str, dict[str, int]] = {}
    for source in ("G", "W"):
        for cell in CELLS:
            chart_id = f"{source}:{cell}"
            chart_counts: dict[str, int] = {}
            for target in TARGETS:
                classification, _proof = classify(source, cell, target)
                chart_counts[classification] = chart_counts.get(classification, 0) + 1
            assert sum(chart_counts.values()) == 162
            counts[chart_id] = chart_counts
    return counts


def main() -> None:
    counts = verify_candidate_table()
    total_retained = 0
    total_empty = 0
    print("GATE3_EIGHT_CHART_CANDIDATE_REDUCTION: CERTIFIED")
    for chart_id in (f"{source}:{cell}" for source in ("G", "W") for cell in CELLS):
        row = counts[chart_id]
        retained = row.get("retained_candidate", 0)
        empty = 162 - retained
        total_retained += retained
        total_empty += empty
        print(
            f"  {chart_id}: retained={retained}, empty={empty}, "
            f"self={row.get('self_source', 0)}, "
            f"horizon={row.get('empty_horizon_center_distance', 0)}, "
            f"outgoing={row.get('empty_outgoing_halfspace', 0)}, "
            f"classification_sha256={canonical_digest(classification_rows(chart_id))}, "
            f"candidate_sha256={canonical_digest(candidate_ids(chart_id))}"
        )
    assert total_retained == 448
    assert total_empty == 848
    print(f"  chart_target_pairs=1296 retained={total_retained} empty={total_empty}")

    # These boxes have nonzero width.  The full s-window is retained even
    # where it cancels algebraically, making the parameter quantifier explicit.
    patches = (
        (
            PhaseBox(
                "G:E",
                -Q(1, 1000),
                Q(1, 1000),
                -Q(1, 1000),
                Q(1, 1000),
                -EPS,
                EPS,
            ),
            "G[1,0]",
            (Q(279, 1000), Q(281, 1000)),
        ),
        (
            PhaseBox(
                "W:E",
                -Q(1, 1000),
                Q(1, 1000),
                -Q(1, 1000),
                Q(1, 1000),
                -EPS,
                EPS,
            ),
            "W[1,0]",
            (Q(67, 100), Q(69, 100)),
        ),
    )
    print("GATE3_LOCAL_FIRST_HIT_PATCHES: CERTIFIED")
    for box, selected, (root_lower, root_upper) in patches:
        root, missed, later = certify_first_hit_patch(box, selected)
        assert bool(root > arbq(root_lower))
        assert bool(root < arbq(root_upper))
        print(
            f"  {box.chart_id}: target={selected}, "
            f"root_in=({root_lower},{root_upper}), Arb_root={root}, "
            f"competitors_missed={missed}, competitors_later={later}"
        )
    print("GATE3_GLOBAL_EVENT_MANIFEST_DQ_MATCHING: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
