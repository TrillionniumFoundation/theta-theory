#!/usr/bin/env python3
"""Rigorous uniform horizon and target-lift box for the standard section.

The actual white disk has radius 4/25 and its center is at distance at most
1/200 from the nominal half-lattice center.  It therefore contains the fixed
core disk of radius 31/200 about that nominal center.  Together with the gray
disks of radius 9/25 this script proves that every unit-speed line issued from
[0,1]^2 enters one of these fixed cores at a time in [3/4,3].  Since 3/4 is
larger than the diameter 18/25 of every core, the witnessed disk cannot merely
be the same disk still containing the starting point.  Hence every physical
free flight is shorter than 3, uniformly in the white-center displacement.

The proof is a finite adaptive cover of

    [0,1] x [0,1] x (R / 2*pi*Z).

Each leaf box carries one fixed rational witness time and one fixed disk.  Arb
interval arithmetic proves that every ray in that whole box lies strictly
inside the disk at the witness time.  Dyadic initial boxes and binary splits
give exact coverage.

The resulting conservative target-lift universe, for a source lift in the
unit square, is the pair of index boxes [-4,4]^2 for gray and white centers.
This certificate does not construct source phase charts, first-hit rows,
event incidences, DQ currents, or occurrence matching.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx


ctx.prec = 160

R_GRAY = Fraction(9, 25)
R_WHITE = Fraction(4, 25)
EPS = Fraction(1, 200)
R_WHITE_CORE = R_WHITE - EPS
T_MIN = Fraction(3, 4)
T_MAX = Fraction(3, 1)

INITIAL_X = 8
INITIAL_Y = 8
INITIAL_ANGLE = 128
MAX_DEPTH = 24


@dataclass(frozen=True)
class Box:
    x0: Fraction
    x1: Fraction
    y0: Fraction
    y1: Fraction
    a0: Fraction  # fraction of one full turn
    a1: Fraction
    depth: int


def arbq(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def interval(center: Fraction, radius: Fraction) -> arb:
    return arbq(center) + arb(0, arbq(radius).upper())


def cores() -> list[tuple[Fraction, Fraction, Fraction, str]]:
    result: list[tuple[Fraction, Fraction, Fraction, str]] = []
    # The enlarged scan box is finite and safely contains every disk that can
    # meet a length-three segment issued from the unit square.
    for i in range(-4, 5):
        for j in range(-4, 5):
            result.append((Fraction(i), Fraction(j), R_GRAY, f"G[{i},{j}]"))
            result.append(
                (
                    Fraction(2 * i + 1, 2),
                    Fraction(2 * j + 1, 2),
                    R_WHITE_CORE,
                    f"Wcore[{i},{j}]",
                )
            )
    return result


CORES = cores()


def midpoint(box: Box) -> tuple[Fraction, Fraction, Fraction]:
    return (
        (box.x0 + box.x1) / 2,
        (box.y0 + box.y1) / 2,
        (box.a0 + box.a1) / 2,
    )


def choose_witness(
    box: Box,
) -> tuple[Fraction, Fraction, Fraction, Fraction, str]:
    """Choose a candidate using doubles; the subsequent Arb test is decisive."""

    xq, yq, aq = midpoint(box)
    x = float(xq)
    y = float(yq)
    theta = 2.0 * math.pi * float(aq)
    ux, uy = math.cos(theta), math.sin(theta)
    best: tuple[float, tuple[Fraction, Fraction, Fraction, Fraction, str]] | None = None
    for cx, cy, radius, label in CORES:
        projection = (float(cx) - x) * ux + (float(cy) - y) * uy
        time_float = min(float(T_MAX), max(float(T_MIN), projection))
        dx = x + time_float * ux - float(cx)
        dy = y + time_float * uy - float(cy)
        margin = float(radius) - math.hypot(dx, dy)
        time = Fraction.from_float(time_float)
        candidate = (cx, cy, radius, time, label)
        if best is None or margin > best[0]:
            best = (margin, candidate)
    assert best is not None
    return best[1]


def arb_witness(box: Box, witness: tuple[Fraction, Fraction, Fraction, Fraction, str]) -> bool:
    cx, cy, radius, time, _label = witness
    x_center, y_center, angle_center = midpoint(box)
    x = interval(x_center, (box.x1 - box.x0) / 2)
    y = interval(y_center, (box.y1 - box.y0) / 2)
    angle_mid = 2 * arb.pi() * arbq(angle_center)
    angle_radius = 2 * arb.pi() * arbq((box.a1 - box.a0) / 2)
    theta = angle_mid + arb(0, angle_radius.upper())
    t = arbq(time)
    dx = x + t * theta.cos() - arbq(cx)
    dy = y + t * theta.sin() - arbq(cy)
    distance_squared = dx * dx + dy * dy
    radius_squared = arbq(radius) * arbq(radius)
    return bool(distance_squared < radius_squared)


def split(box: Box) -> tuple[Box, Box]:
    x_width = box.x1 - box.x0
    y_width = box.y1 - box.y0
    # Angular uncertainty contributes at most T_MAX times its radian width.
    angle_weight = float(T_MAX) * 2.0 * math.pi * float(box.a1 - box.a0)
    weights = (float(x_width), float(y_width), angle_weight)
    axis = max(range(3), key=weights.__getitem__)
    depth = box.depth + 1
    if axis == 0:
        middle = (box.x0 + box.x1) / 2
        return (
            Box(box.x0, middle, box.y0, box.y1, box.a0, box.a1, depth),
            Box(middle, box.x1, box.y0, box.y1, box.a0, box.a1, depth),
        )
    if axis == 1:
        middle = (box.y0 + box.y1) / 2
        return (
            Box(box.x0, box.x1, box.y0, middle, box.a0, box.a1, depth),
            Box(box.x0, box.x1, middle, box.y1, box.a0, box.a1, depth),
        )
    middle = (box.a0 + box.a1) / 2
    return (
        Box(box.x0, box.x1, box.y0, box.y1, box.a0, middle, depth),
        Box(box.x0, box.x1, box.y0, box.y1, middle, box.a1, depth),
    )


def initial_boxes() -> list[Box]:
    return [
        Box(
            Fraction(i, INITIAL_X),
            Fraction(i + 1, INITIAL_X),
            Fraction(j, INITIAL_Y),
            Fraction(j + 1, INITIAL_Y),
            Fraction(k, INITIAL_ANGLE),
            Fraction(k + 1, INITIAL_ANGLE),
            0,
        )
        for i in range(INITIAL_X)
        for j in range(INITIAL_Y)
        for k in range(INITIAL_ANGLE)
    ]


def certify_cover() -> tuple[int, int, dict[str, int]]:
    pending = initial_boxes()
    leaves = 0
    maximum_depth = 0
    witness_counts: dict[str, int] = {}
    while pending:
        box = pending.pop()
        witness = choose_witness(box)
        if arb_witness(box, witness):
            leaves += 1
            maximum_depth = max(maximum_depth, box.depth)
            witness_counts[witness[4]] = witness_counts.get(witness[4], 0) + 1
            continue
        if box.depth >= MAX_DEPTH:
            raise RuntimeError(f"unresolved horizon box at depth {box.depth}: {box}")
        pending.extend(split(box))
    return leaves, maximum_depth, witness_counts


def certify_lift_bounds() -> None:
    # Any hit point lies coordinatewise in [-3,4].  A gray target center lies
    # within R_GRAY of it; every possible integer is therefore in [-3,4], a
    # subset of the declared [-4,4].
    gray_lower = -T_MAX - R_GRAY
    gray_upper = 1 + T_MAX + R_GRAY
    assert gray_lower > -4
    assert gray_upper < 5

    # The nominal half-lattice white center is within EPS of the actual center,
    # and the actual center is within R_WHITE of the hit point.  The declared
    # half-lattice index box [-4,4]^2 is again a conservative superset.
    white_nominal_lower = -T_MAX - R_WHITE - EPS
    white_nominal_upper = 1 + T_MAX + R_WHITE + EPS
    assert white_nominal_lower > Fraction(-7, 2)
    assert white_nominal_upper < Fraction(9, 2)


def main() -> None:
    assert R_WHITE_CORE == Fraction(31, 200)
    assert T_MIN > 2 * max(R_GRAY, R_WHITE_CORE)
    leaves, maximum_depth, witness_counts = certify_cover()
    certify_lift_bounds()
    print("STANDARD_SECTION_UNIFORM_HORIZON: CERTIFIED")
    print("  white_fixed_core_radius=31/200")
    print("  every_ray_hit_window=[3/4,3]")
    print("  tau_max<3")
    print(f"  certified_leaf_boxes={leaves}")
    print(f"  maximum_binary_depth={maximum_depth}")
    print(f"  distinct_witness_disks={len(witness_counts)}")
    print("STANDARD_SECTION_TARGET_LIFT_BOX: CERTIFIED")
    print("  gray_indices=[-4,4]^2")
    print("  white_indices=[-4,4]^2")
    print("GLOBAL_EVENT_MANIFEST: NOT CERTIFIED")


if __name__ == "__main__":
    main()
