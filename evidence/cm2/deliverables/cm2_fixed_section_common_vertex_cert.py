#!/usr/bin/env python3
"""Rigorous local connector certificate for the rational fixed-section pilot.

This script certifies three finite statements at the centered table c=0:

* ``ORBIT_ROOT``: existence and uniqueness of a symmetric periodic
  specular orbit for the displayed gray/white collision word;
* ``PHYSICAL_WORD``: that this orbit follows the declared first-collision
  itinerary, stays away from transparent walls, and is uniformly
  non-grazing;
* ``TRIVIALIZED_MATRIX_NONDEGENERACY``: the derivative of the resulting period-eight
  fixed-section loop, expressed in the same gray arclength--momentum chart
  as the exact gray--white loop, is positive, proximal, and twists all four
  stable/unstable eigenline pairs.

It deliberately does *not* certify a common full-cross Markov rectangle or
a lower bound for the conditional Gibbs weights.  Those two missing layers
are printed as ``NOT CERTIFIED`` and are not implied by the periodic-orbit
calculation.

Dependency
----------

    python-flint == 0.9.0

The calculation uses Arb balls through python-flint.  It has no floating
point acceptance test: every successful comparison is a strict Arb-ball
comparison.  The decimal strings below are merely centers of rational
input balls; the Krawczyk inclusion proves that a true root lies in those
balls.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence

try:
    import flint
    from flint import arb, arb_mat, ctx, fmpq
except ImportError as exc:  # pragma: no cover - dependency diagnostic
    print(
        "DEPENDENCY_FAILURE: install python-flint==0.9.0 "
        "(for example: python -m pip install 'python-flint==0.9.0')",
        file=sys.stderr,
    )
    raise SystemExit(2) from exc


# Four hundred bits leave a large margin beyond the 1e-50 root boxes.
ctx.prec = 400

if flint.__version__ != "0.9.0":
    print(
        "DEPENDENCY_FAILURE: this frozen certificate requires "
        f"python-flint==0.9.0, found {flint.__version__}",
        file=sys.stderr,
    )
    raise SystemExit(2)

ZERO = arb(0)
ONE = arb(1)
HALF = ONE / 2
R_GRAY = arb(9) / 25
R_WHITE = arb(4) / 25
ROOT_RADIUS = "1e-50"
PRECONDITIONER_DECIMAL_DIGITS = 70


@dataclass(frozen=True)
class Obstacle:
    kind: str
    i: int
    j: int
    center: tuple[arb, arb]
    radius: arb


def obstacle(kind: str, i: int, j: int) -> Obstacle:
    if kind == "G":
        return Obstacle(kind, i, j, (arb(i), arb(j)), R_GRAY)
    if kind == "W":
        return Obstacle(
            kind,
            i,
            j,
            (arb(i) + HALF, arb(j) + HALF),
            R_WHITE,
        )
    raise ValueError(f"unknown obstacle kind {kind!r}")


# The full symmetric collision word is
# G0 W0 G0 W0 G0 W0 G1 G0 G1 W0 G0 W0 G0 W0, then back to G0.
# White collisions are not returns of Stenlund's fixed-section map, so this
# is a period-eight word for that map.
HALF_KEYS: tuple[tuple[str, int, int], ...] = (
    ("G", 0, 0),
    ("W", 0, 0),
    ("G", 0, 0),
    ("W", 0, 0),
    ("G", 0, 0),
    ("W", 0, 0),
    ("G", 1, 0),
    ("G", 0, 0),
)
FULL_KEYS = HALF_KEYS + tuple(reversed(HALF_KEYS[1:-1]))
HALF_OBSTACLES = tuple(obstacle(*key) for key in HALF_KEYS)
FULL_OBSTACLES = tuple(obstacle(*key) for key in FULL_KEYS)


# Outward-normal angles for the eight independent collisions of the
# half-orbit.  The other six angles are obtained by reflection of the word.
ROOT_CENTERS: tuple[str, ...] = (
    "0.78409255751959244111062347294760048351680250557700470160436187178052747618097046",
    "-2.3517300483808756698565855798408794460655172525076753820903027700405392228116093",
    "0.77809412020391269611509721386559627419250016026494393820400248950852844564439473",
    "-2.3106602419244545214875686925094193091540621819350906307799844657156255285691045",
    "0.70412530822095186665118117469818340796812603726352866570416690454201969142622801",
    "-1.749547624728970974726108339688884325290151738599456051751896185985900360587972",
    "2.7996974483111616287218404650974684788259962283643461264708271031714101301143835",
    "0.18065356593169448698888272139194277712932390782134554478210956355385939048489173",
)


def ball_abs_lower_than_zero(value: arb) -> bool:
    """Return True precisely when the ball is proved disjoint from zero."""

    return not value.contains(0)


def strict_between(value: arb, lower: arb, upper: arb) -> bool:
    return value > lower and value < upper


class Dual:
    """First-order Arb dual number with a fixed derivative dimension."""

    __slots__ = ("value", "derivative")

    def __init__(
        self,
        value: arb | int,
        derivative: Sequence[arb] | None = None,
        dimension: int = 0,
    ) -> None:
        self.value = value if isinstance(value, arb) else arb(value)
        self.derivative = (
            list(derivative)
            if derivative is not None
            else [arb(0) for _ in range(dimension)]
        )

    @property
    def dimension(self) -> int:
        return len(self.derivative)

    def coerce(self, other: Dual | arb | int) -> Dual:
        if isinstance(other, Dual):
            if other.dimension != self.dimension:
                raise ValueError("incompatible dual dimensions")
            return other
        return Dual(other, dimension=self.dimension)

    def __add__(self, other: Dual | arb | int) -> Dual:
        other = self.coerce(other)
        return Dual(
            self.value + other.value,
            [a + b for a, b in zip(self.derivative, other.derivative)],
        )

    __radd__ = __add__

    def __neg__(self) -> Dual:
        return Dual(-self.value, [-entry for entry in self.derivative])

    def __sub__(self, other: Dual | arb | int) -> Dual:
        return self + (-self.coerce(other))

    def __rsub__(self, other: Dual | arb | int) -> Dual:
        return self.coerce(other) - self

    def __mul__(self, other: Dual | arb | int) -> Dual:
        other = self.coerce(other)
        return Dual(
            self.value * other.value,
            [
                left * other.value + self.value * right
                for left, right in zip(self.derivative, other.derivative)
            ],
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Dual | arb | int) -> Dual:
        other = self.coerce(other)
        denominator = other.value * other.value
        return Dual(
            self.value / other.value,
            [
                (left * other.value - self.value * right) / denominator
                for left, right in zip(self.derivative, other.derivative)
            ],
        )

    def __rtruediv__(self, other: Dual | arb | int) -> Dual:
        return self.coerce(other) / self


def dual_sin(value: Dual) -> Dual:
    return Dual(
        value.value.sin(),
        [value.value.cos() * entry for entry in value.derivative],
    )


def dual_cos(value: Dual) -> Dual:
    return Dual(
        value.value.cos(),
        [-value.value.sin() * entry for entry in value.derivative],
    )


def dual_sqrt(value: Dual) -> Dual:
    root = value.value.sqrt()
    return Dual(root, [entry / (2 * root) for entry in value.derivative])


def dual_dot(
    left: tuple[Dual, Dual], right: tuple[Dual, Dual]
) -> Dual:
    return left[0] * right[0] + left[1] * right[1]


def dual_unit(
    source: tuple[Dual, Dual], target: tuple[Dual, Dual]
) -> tuple[Dual, Dual]:
    difference = (target[0] - source[0], target[1] - source[1])
    length = dual_sqrt(dual_dot(difference, difference))
    return difference[0] / length, difference[1] / length


def half_orbit_equations(
    angles: Sequence[arb], with_derivative: bool
) -> tuple[list[arb], list[list[arb]]]:
    """Return the eight symmetric half-orbit equations and Jacobian."""

    dimension = len(angles)
    theta: list[Dual] = []
    for index, angle in enumerate(angles):
        derivative = [arb(0) for _ in range(dimension)]
        if with_derivative:
            derivative[index] = arb(1)
        theta.append(Dual(angle, derivative))

    points: list[tuple[Dual, Dual]] = []
    tangents: list[tuple[Dual, Dual]] = []
    for angle, target in zip(theta, HALF_OBSTACLES):
        normal = dual_cos(angle), dual_sin(angle)
        points.append(
            (
                target.center[0] + target.radius * normal[0],
                target.center[1] + target.radius * normal[1],
            )
        )
        tangents.append((-normal[1], normal[0]))

    flights = [
        dual_unit(points[index], points[index + 1])
        for index in range(len(points) - 1)
    ]

    # Reflection symmetry makes the first and last collisions normal.  The
    # six interior equations impose equality of incoming/outgoing tangential
    # components.
    equations = [dual_dot(tangents[0], flights[0])]
    for index in range(1, len(points) - 1):
        equations.append(
            dual_dot(
                tangents[index],
                (
                    flights[index - 1][0] - flights[index][0],
                    flights[index - 1][1] - flights[index][1],
                ),
            )
        )
    equations.append(dual_dot(tangents[-1], flights[-1]))
    return (
        [entry.value for entry in equations],
        [entry.derivative for entry in equations],
    )


@dataclass
class RootCertificate:
    centers: list[arb]
    boxes: list[arb]
    krawczyk: arb_mat
    jacobian_determinant: arb


def certify_orbit_root() -> RootCertificate:
    centers = [arb(value) for value in ROOT_CENTERS]
    boxes = [arb(value, ROOT_RADIUS) for value in ROOT_CENTERS]

    values, jacobian_center = half_orbit_equations(centers, True)
    _, jacobian_box = half_orbit_equations(boxes, True)
    f_center = arb_mat([[entry] for entry in values])
    j_center = arb_mat(jacobian_center)
    j_box = arb_mat(jacobian_box)
    inverse_enclosure = j_center.inv()

    # Freeze one point preconditioner for the Krawczyk theorem.  Each entry
    # is an exact decimal rational obtained from the midpoint of the center
    # inverse, rather than an interval inverse varying over the Jacobian box.
    preconditioner_rows: list[list[arb]] = []
    for row in range(len(centers)):
        entries: list[arb] = []
        for column in range(len(centers)):
            decimal = inverse_enclosure[row, column].str(
                PRECONDITIONER_DECIMAL_DIGITS,
                radius=False,
                more=True,
            )
            rational = Fraction(decimal)
            entries.append(arb(fmpq(rational.numerator, rational.denominator)))
        preconditioner_rows.append(entries)
    preconditioner = arb_mat(preconditioner_rows)

    identity = arb_mat(len(centers), len(centers))
    for index in range(len(centers)):
        identity[index, index] = arb(1)

    center_vector = arb_mat([[entry] for entry in centers])
    centered_box = arb_mat(
        [[arb(0, ROOT_RADIUS)] for _ in range(len(centers))]
    )
    krawczyk = (
        center_vector
        - preconditioner * f_center
        + (identity - preconditioner * j_box) * centered_box
    )

    inclusion = all(
        boxes[index].contains_interior(krawczyk[index, 0])
        for index in range(len(boxes))
    )
    determinant = j_center.det()
    if not inclusion:
        raise RuntimeError("Krawczyk image is not interior to the root box")
    if determinant.contains(0):
        raise RuntimeError("half-orbit Jacobian determinant may vanish")
    if not abs(determinant) > 8500:
        raise RuntimeError(
            "half-orbit Jacobian determinant is not separated by 8500: "
            f"{determinant}"
        )
    if preconditioner.det().contains(0):
        raise RuntimeError("fixed rational Krawczyk preconditioner may be singular")

    print("ORBIT_ROOT: CERTIFIED")
    print(f"  python-flint={flint.__version__}, arb_precision_bits={ctx.prec}")
    print(f"  root_box_radius={ROOT_RADIUS}")
    print(
        "  fixed_rational_preconditioner_decimal_digits="
        f"{PRECONDITIONER_DECIMAL_DIGITS}"
    )
    print(f"  half_orbit_jacobian_determinant={determinant}")
    print(f"  maximum_center_residual={max(abs(entry) for entry in values)}")
    return RootCertificate(centers, boxes, krawczyk, determinant)


def arb_dot(
    left: tuple[arb, arb], right: tuple[arb, arb]
) -> arb:
    return left[0] * right[0] + left[1] * right[1]


def arb_unit(
    source: tuple[arb, arb], target: tuple[arb, arb]
) -> tuple[arb, arb]:
    difference = target[0] - source[0], target[1] - source[1]
    length = arb_dot(difference, difference).sqrt()
    return difference[0] / length, difference[1] / length


def collision_points(
    angle_boxes: Sequence[arb], targets: Sequence[Obstacle]
) -> tuple[list[tuple[arb, arb]], list[tuple[arb, arb]]]:
    points: list[tuple[arb, arb]] = []
    normals: list[tuple[arb, arb]] = []
    for angle, target in zip(angle_boxes, targets):
        normal = angle.cos(), angle.sin()
        normals.append(normal)
        points.append(
            (
                target.center[0] + target.radius * normal[0],
                target.center[1] + target.radius * normal[1],
            )
        )
    return points, normals


def minimum_line_segment_distance_squared(
    source: tuple[arb, arb],
    target: tuple[arb, arb],
    center: tuple[arb, arb],
) -> arb:
    """A rigorous squared distance to a segment.

    When the projection ball is undecided at an endpoint, the infinite-line
    distance is used.  That is always a valid lower bound for the segment
    distance, although it can be conservative.
    """

    direction = target[0] - source[0], target[1] - source[1]
    source_to_center = center[0] - source[0], center[1] - source[1]
    denominator = arb_dot(direction, direction)
    projection = arb_dot(source_to_center, direction) / denominator
    if projection < 0:
        return arb_dot(source_to_center, source_to_center)
    if projection > 1:
        target_to_center = center[0] - target[0], center[1] - target[1]
        return arb_dot(target_to_center, target_to_center)
    perpendicular = (
        arb_dot(source_to_center, source_to_center)
        - arb_dot(source_to_center, direction) ** 2 / denominator
    )
    return perpendicular


def all_lattice_obstacles() -> Iterable[Obstacle]:
    # The separate lattice-exhaustion check proves that every center omitted
    # here is farther than the required clearance from the entire certified
    # flight rectangle.
    for kind in ("G", "W"):
        for i in range(-3, 4):
            for j in range(-3, 4):
                yield obstacle(kind, i, j)


def certify_lattice_exhaustion(clearance_threshold: arb) -> None:
    """Prove that the finite lift enumeration exhausts possible first hits.

    Every certified flight is contained in
    [1/20,3/4] x [1/20,1/2].  If a gray or white lift has an index outside
    [-3,3] in either coordinate, its center is separated from this rectangle
    in that coordinate by more than 13/4.  Since the largest obstacle radius
    is 9/25, every omitted lift has clearance greater than
    13/4 - 9/25 > 1/5.  These are exact rational inequalities.
    """

    exterior_center_distance = arb(13) / 4
    if not exterior_center_distance - R_GRAY > clearance_threshold:
        raise RuntimeError("finite lattice enumeration has no exterior margin")


def same_obstacle(left: Obstacle, right: Obstacle) -> bool:
    return (left.kind, left.i, left.j) == (right.kind, right.i, right.j)


def certify_physical_word(root: RootCertificate) -> None:
    full_angles = root.boxes + list(reversed(root.boxes[1:-1]))
    points, normals = collision_points(full_angles, FULL_OBSTACLES)

    # Every point is strictly inside one convex fundamental square, so every
    # chord between consecutive points misses the transparent square walls.
    for point in points:
        if not strict_between(point[0], arb(1) / 20, arb(3) / 4):
            raise RuntimeError(f"x-coordinate leaves the certified square: {point[0]}")
        if not strict_between(point[1], arb(1) / 20, arb(1) / 2):
            raise RuntimeError(f"y-coordinate leaves the certified square: {point[1]}")

    incidence_threshold = arb(3) / 5
    clearance_threshold = arb(1) / 5
    certify_lattice_exhaustion(clearance_threshold)
    minimum_departure: arb | None = None
    minimum_arrival: arb | None = None
    minimum_clearance: arb | None = None

    lattice = tuple(all_lattice_obstacles())
    count = len(points)
    for index in range(count):
        next_index = (index + 1) % count
        source = points[index]
        target = points[next_index]
        velocity = arb_unit(source, target)
        departure = arb_dot(velocity, normals[index])
        arrival = -arb_dot(velocity, normals[next_index])
        if not departure > incidence_threshold:
            raise RuntimeError(
                f"departure incidence fails on segment {index}: {departure}"
            )
        if not arrival > incidence_threshold:
            raise RuntimeError(
                f"arrival incidence fails on segment {index}: {arrival}"
            )
        minimum_departure = (
            departure
            if minimum_departure is None or departure < minimum_departure
            else minimum_departure
        )
        minimum_arrival = (
            arrival
            if minimum_arrival is None or arrival < minimum_arrival
            else minimum_arrival
        )

        source_obstacle = FULL_OBSTACLES[index]
        target_obstacle = FULL_OBSTACLES[next_index]
        for candidate in lattice:
            if same_obstacle(candidate, source_obstacle) or same_obstacle(
                candidate, target_obstacle
            ):
                continue
            distance_squared = minimum_line_segment_distance_squared(
                source, target, candidate.center
            )
            required = candidate.radius + clearance_threshold
            if not distance_squared > required * required:
                raise RuntimeError(
                    "unintended obstacle clearance fails on segment "
                    f"{index} against {(candidate.kind, candidate.i, candidate.j)}: "
                    f"distance_squared={distance_squared}"
                )
            clearance = distance_squared.sqrt() - candidate.radius
            minimum_clearance = (
                clearance
                if minimum_clearance is None or clearance < minimum_clearance
                else minimum_clearance
            )

    print("PHYSICAL_WORD: CERTIFIED")
    print("  fixed_section_return_period=8, solid_collision_count=14")
    print(f"  incidence_cosine_threshold>{incidence_threshold}")
    print(f"  minimum_departure_cosine={minimum_departure}")
    print(f"  minimum_arrival_cosine={minimum_arrival}")
    print(f"  unintended_obstacle_clearance_threshold>{clearance_threshold}")
    print(f"  certified_minimum_unintended_clearance={minimum_clearance}")
    print("  omitted_lift_center_distance>13/4")
    print("  transparent_wall_crossings=0")


def ray_circle_collision(
    position: tuple[Dual, Dual],
    velocity: tuple[Dual, Dual],
    target: Obstacle,
) -> tuple[tuple[Dual, Dual], tuple[Dual, Dual]]:
    displacement = (
        position[0] - target.center[0],
        position[1] - target.center[1],
    )
    linear = dual_dot(displacement, velocity)
    offset = dual_dot(displacement, displacement) - target.radius**2
    discriminant = linear * linear - offset
    if not discriminant.value > 0:
        raise RuntimeError(f"nonpositive collision discriminant: {discriminant.value}")
    flight = -linear - dual_sqrt(discriminant)
    if not flight.value > 0:
        raise RuntimeError(f"selected collision root is not forward: {flight.value}")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    normal = (
        (impact[0] - target.center[0]) / target.radius,
        (impact[1] - target.center[1]) / target.radius,
    )
    normal_speed = dual_dot(velocity, normal)
    reflected = (
        velocity[0] - 2 * normal_speed * normal[0],
        velocity[1] - 2 * normal_speed * normal[1],
    )
    return impact, reflected


def connector_derivative(base_angle: arb) -> tuple[arb_mat, arb, arb]:
    """Differentiate the full word in gray arclength--momentum coordinates."""

    arclength = Dual(arb(0), [arb(1), arb(0)])
    momentum = Dual(arb(0), [arb(0), arb(1)])
    theta = Dual(base_angle, [arb(0), arb(0)]) + arclength / R_GRAY
    normal = dual_cos(theta), dual_sin(theta)
    tangent = -normal[1], normal[0]
    cosine_phi = dual_sqrt(1 - momentum * momentum)
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    first = FULL_OBSTACLES[0]
    position = (
        first.center[0] + first.radius * normal[0],
        first.center[1] + first.radius * normal[1],
    )

    for target in FULL_OBSTACLES[1:] + FULL_OBSTACLES[:1]:
        position, velocity = ray_circle_collision(position, velocity, target)

    final_normal = (
        (position[0] - first.center[0]) / first.radius,
        (position[1] - first.center[1]) / first.radius,
    )
    final_tangent = -final_normal[1], final_normal[0]
    # d atan2(n_y,n_x) = n_x d n_y - n_y d n_x on the unit circle.
    angle_derivative = [
        final_normal[0].value * final_normal[1].derivative[index]
        - final_normal[1].value * final_normal[0].derivative[index]
        for index in range(2)
    ]
    final_momentum = dual_dot(velocity, final_tangent)
    matrix = arb_mat(
        [
            [R_GRAY * angle_derivative[0], R_GRAY * angle_derivative[1]],
            [final_momentum.derivative[0], final_momentum.derivative[1]],
        ]
    )
    # At the certified root the symmetric word returns to the initial point.
    # The two balls below are diagnostics; their containment of zero is also
    # checked in the matrix layer.
    final_angle = arb.atan2(final_normal[1].value, final_normal[0].value)
    angle_residual = final_angle - base_angle
    momentum_residual = final_momentum.value
    return matrix, angle_residual, momentum_residual


def determinant_pair(left: tuple[arb, arb], right: tuple[arb, arb]) -> arb:
    return left[0] * right[1] - left[1] * right[0]


def matrix_vector(matrix: arb_mat, vector: tuple[arb, arb]) -> tuple[arb, arb]:
    return (
        matrix[0, 0] * vector[0] + matrix[0, 1] * vector[1],
        matrix[1, 0] * vector[0] + matrix[1, 1] * vector[1],
    )


def certify_trivialized_matrix_nondegeneracy(root: RootCertificate) -> None:
    matrix_b, angle_residual, momentum_residual = connector_derivative(
        root.boxes[0]
    )
    if not angle_residual.contains(0):
        raise RuntimeError(f"periodic angle residual misses zero: {angle_residual}")
    if not momentum_residual.contains(0):
        raise RuntimeError(
            f"periodic momentum residual misses zero: {momentum_residual}"
        )

    sqrt_two = arb(2).sqrt()
    alpha = (arb(661) - 325 * sqrt_two) / 36
    beta = (arb(859) - 550 * sqrt_two) / 100
    gamma = arb(625) * (25 - 4 * sqrt_two) / 324
    matrix_a = arb_mat([[alpha, beta], [gamma, alpha]])

    entry_boxes = (
        (matrix_b[0, 0], arb(53_749_822), arb(53_749_823)),
        (matrix_b[0, 1], arb(7_928_332), arb(7_928_334)),
        (matrix_b[1, 0], arb(364_394_816), arb(364_394_818)),
        (matrix_b[1, 1], arb(53_749_822), arb(53_749_823)),
    )
    for entry, lower, upper in entry_boxes:
        if not strict_between(entry, lower, upper):
            raise RuntimeError(
                f"connector derivative entry leaves ({lower},{upper}): {entry}"
            )

    determinant_b = matrix_b.det()
    if not strict_between(determinant_b, arb(999) / 1000, arb(1001) / 1000):
        raise RuntimeError(f"connector determinant is not near one: {determinant_b}")
    if not matrix_b[0, 0] + matrix_b[1, 1] > arb(100_000_000):
        raise RuntimeError("connector loop is not certified proximal")

    slope = (gamma / beta).sqrt()
    unstable = arb(1), slope
    stable = arb(1), -slope
    b_unstable = matrix_vector(matrix_b, unstable)
    b_stable = matrix_vector(matrix_b, stable)
    twisting = {
        "det(v_plus,J_B v_plus)": determinant_pair(unstable, b_unstable),
        "det(v_minus,J_B v_plus)": determinant_pair(stable, b_unstable),
        "det(v_plus,J_B v_minus)": determinant_pair(unstable, b_stable),
        "det(v_minus,J_B v_minus)": determinant_pair(stable, b_stable),
    }
    lower_bounds = {
        "det(v_plus,J_B v_plus)": arb(7000),
        "det(v_minus,J_B v_plus)": arb(1_000_000_000),
        "det(v_plus,J_B v_minus)": arb(3) / 100,
        "det(v_minus,J_B v_minus)": arb(7000),
    }
    for name, value in twisting.items():
        if not ball_abs_lower_than_zero(value):
            raise RuntimeError(f"twisting determinant may vanish: {name}={value}")
        if not abs(value) > lower_bounds[name]:
            raise RuntimeError(
                f"twisting margin below threshold: {name}={value}, "
                f"threshold={lower_bounds[name]}"
            )

    eigenline_obstruction = gamma * matrix_b[0, 1] - matrix_b[1, 0] * beta
    if not eigenline_obstruction > 6000:
        raise RuntimeError(
            f"eigenline obstruction is not >6000: {eigenline_obstruction}"
        )

    print("TRIVIALIZED_MATRIX_NONDEGENERACY: CERTIFIED")
    print("  scope=centered table and common gray arclength--momentum chart")
    print(f"  J_A={matrix_a}")
    print(f"  J_B={matrix_b}")
    print(f"  det_J_B={determinant_b}")
    print(f"  eigenline_obstruction={eigenline_obstruction}")
    for name, value in twisting.items():
        print(f"  {name}={value}")


def main() -> int:
    try:
        root = certify_orbit_root()
    except Exception as exc:  # exact failure label for automation
        print(f"ORBIT_ROOT: FAILED: {exc}")
        print("PHYSICAL_WORD: NOT RUN")
        print("TRIVIALIZED_MATRIX_NONDEGENERACY: NOT RUN")
        print("COMMON_MAGNET: NOT CERTIFIED")
        print("GIBBS_PHYSICAL_ID: NOT CERTIFIED")
        return 1

    try:
        certify_physical_word(root)
    except Exception as exc:
        print(f"PHYSICAL_WORD: FAILED: {exc}")
        print("TRIVIALIZED_MATRIX_NONDEGENERACY: NOT RUN")
        print("COMMON_MAGNET: NOT CERTIFIED")
        print("GIBBS_PHYSICAL_ID: NOT CERTIFIED")
        return 1

    try:
        certify_trivialized_matrix_nondegeneracy(root)
    except Exception as exc:
        print(f"TRIVIALIZED_MATRIX_NONDEGENERACY: FAILED: {exc}")
        print("COMMON_MAGNET: NOT CERTIFIED")
        print("GIBBS_PHYSICAL_ID: NOT CERTIFIED")
        return 1

    print(
        "COMMON_MAGNET: NOT CERTIFIED "
        "(full-cross strips, cone graph transform, and singularity margins remain)"
    )
    print(
        "GIBBS_PHYSICAL_ID: NOT CERTIFIED "
        "(conditional strip weights and endpoint projective identification remain)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
