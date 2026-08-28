#!/usr/bin/env python3
"""Rigorous tangent-line matching seed near the QNL and connector centers.

The certificate solves a two-parameter matching equation.  Starting on the
QNL unstable tangent at ``G(0,0)``, it follows five gray--white cycles (ten
solid collisions).  Starting on the connector stable tangent, it reverses
the certified fourteen-collision connector word.  The two terminal states
are matched on the gray section.

The two source curves are the *linear eigentangents* at the periodic points,
not validated local invariant-manifold graphs.  Thus a successful run only
certifies a transverse matching of two finite images of those tangent lines,
with a physical immutable word.  It is not a heteroclinic intersection, a
full-cross transition, or a common-magnet theorem.  Those layers are printed
as not certified.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Sequence


FROZEN_CERT = Path(__file__).with_name("cm2_fixed_section_common_vertex_cert.py")
PRECISION_BITS = 400
PRECONDITIONER_DIGITS = 90

# Relative torus lifts after recentering at every solid collision.
QNL_FORWARD_WORD: tuple[tuple[str, int, int], ...] = tuple(
    ("W", 0, 0) if index % 2 == 0 else ("G", 0, 0)
    for index in range(10)
)
CONNECTOR_REVERSE_FORWARD_WORD: tuple[tuple[str, int, int], ...] = (
    ("W", 0, 0),
    ("G", 0, 0),
    ("W", 0, 0),
    ("G", 0, 0),
    ("W", 0, 0),
    ("G", 1, 0),
    ("G", -1, 0),
    ("G", 1, 0),
    ("W", -1, 0),
    ("G", 0, 0),
    ("W", 0, 0),
    ("G", 0, 0),
    ("W", 0, 0),
    ("G", 0, 0),
)
FULL_FORWARD_TRANSITION_WORD = QNL_FORWARD_WORD + CONNECTOR_REVERSE_FORWARD_WORD

# Binary64 discovery seeds; Newton refinement below does not accept them.
T_SEED = "-1.3961010804592166e-9"
U_SEED = "2.186116350289211e-12"


def load_frozen_certificate():
    spec = importlib.util.spec_from_file_location("cm2_v52_common_vertex", FROZEN_CERT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load frozen certificate {FROZEN_CERT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.ctx.prec = PRECISION_BITS
    return module


@dataclass
class PathResult:
    theta: object
    momentum: object
    minima: dict[str, object]
    cumulative_lifts: tuple[tuple[int, int], ...]


def dual_atan2(module, y, x):
    denominator = x.value * x.value + y.value * y.value
    if not denominator > 0:
        raise RuntimeError(f"atan2 denominator is not positive: {denominator}")
    return module.Dual(
        module.arb.atan2(y.value, x.value),
        [
            (x.value * dy - y.value * dx) / denominator
            for dx, dy in zip(x.derivative, y.derivative)
        ],
    )


def update_minimum(current, value):
    return value if current is None else current.min(value)


def same_key(left, right) -> bool:
    return (left.kind, left.i, left.j) == (right.kind, right.i, right.j)


def segment_clearance(module, source, target, source_obstacle, target_obstacle):
    minimum = None
    for candidate in module.all_lattice_obstacles():
        if same_key(candidate, source_obstacle) or same_key(candidate, target_obstacle):
            continue
        distance_squared = module.minimum_line_segment_distance_squared(
            source, target, candidate.center
        )
        if not distance_squared > candidate.radius * candidate.radius:
            raise RuntimeError(
                "unintended obstacle may meet the declared segment: "
                f"source={(source_obstacle.kind, source_obstacle.i, source_obstacle.j)}, "
                f"target={(target_obstacle.kind, target_obstacle.i, target_obstacle.j)}, "
                f"candidate={(candidate.kind, candidate.i, candidate.j)}, "
                f"distance_squared={distance_squared}"
            )
        clearance = distance_squared.sqrt() - candidate.radius
        minimum = update_minimum(minimum, clearance)
    if minimum is None:
        raise RuntimeError("empty unintended-obstacle enumeration")
    return minimum


def initial_state(module, kind: str, theta, momentum):
    normal = module.dual_cos(theta), module.dual_sin(theta)
    tangent = -normal[1], normal[0]
    cosine_phi = module.dual_sqrt(1 - momentum * momentum)
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    source = module.obstacle(kind, 0, 0)
    position = (
        module.Dual(source.center[0], dimension=theta.dimension)
        + source.radius * normal[0],
        module.Dual(source.center[1], dimension=theta.dimension)
        + source.radius * normal[1],
    )
    return position, velocity, source


def propagate(module, kind: str, theta, momentum, word: Sequence[tuple[str, int, int]]):
    position, velocity, source_obstacle = initial_state(module, kind, theta, momentum)
    minima = {"flight": None, "discriminant": None, "incidence": None, "clearance": None}
    cumulative_i = 0
    cumulative_j = 0
    cumulative_lifts = [(0, 0)]

    for target_key in word:
        target_obstacle = module.obstacle(*target_key)
        displacement = (
            position[0] - target_obstacle.center[0],
            position[1] - target_obstacle.center[1],
        )
        linear = module.dual_dot(displacement, velocity)
        offset = (
            module.dual_dot(displacement, displacement)
            - target_obstacle.radius * target_obstacle.radius
        )
        discriminant = linear * linear - offset
        if not discriminant.value > 0:
            raise RuntimeError(f"nonpositive target discriminant: {discriminant.value}")
        flight = -linear - module.dual_sqrt(discriminant)
        if not flight.value > 0:
            raise RuntimeError(f"nonpositive near collision root: {flight.value}")
        impact = (
            position[0] + flight * velocity[0],
            position[1] + flight * velocity[1],
        )
        normal = (
            (impact[0] - target_obstacle.center[0]) / target_obstacle.radius,
            (impact[1] - target_obstacle.center[1]) / target_obstacle.radius,
        )
        incoming = -module.dual_dot(velocity, normal)
        if not incoming.value > 0:
            raise RuntimeError(f"nonpositive incoming incidence: {incoming.value}")

        source_values = (position[0].value, position[1].value)
        target_values = (impact[0].value, impact[1].value)
        # These canonical endpoint bounds make the [-3,3]^2 first-hit
        # enumeration exhaustive.  Any omitted gray lift has an integer
        # coordinate of magnitude at least four and hence coordinate gap at
        # least 5/2 from this box; an omitted white lift has gap at least two.
        # Both are larger than the maximum radius 9/25.
        canonical_bound = module.arb(3) / 2
        for endpoint in (source_values, target_values):
            if not (
                endpoint[0] > -canonical_bound
                and endpoint[0] < canonical_bound
                and endpoint[1] > -canonical_bound
                and endpoint[1] < canonical_bound
            ):
                raise RuntimeError(
                    f"canonical endpoint leaves (-3/2,3/2)^2: {endpoint}"
                )
        clearance = segment_clearance(
            module,
            source_values,
            target_values,
            source_obstacle,
            target_obstacle,
        )
        minima["flight"] = update_minimum(minima["flight"], flight.value)
        minima["discriminant"] = update_minimum(
            minima["discriminant"], discriminant.value
        )
        minima["incidence"] = update_minimum(minima["incidence"], incoming.value)
        minima["clearance"] = update_minimum(minima["clearance"], clearance)

        # The cumulative universal-cover points of both immutable words stay
        # in the open unit square, hence the fixed-section transparent walls
        # are not crossed.  Convexity then handles the whole flight segment.
        global_impact_x = impact[0].value + cumulative_i
        global_impact_y = impact[1].value + cumulative_j
        if not (
            global_impact_x > 0
            and global_impact_x < 1
            and global_impact_y > 0
            and global_impact_y < 1
        ):
            raise RuntimeError(
                f"global impact may leave the open unit square: "
                f"({global_impact_x},{global_impact_y})"
            )

        reflected = (
            velocity[0] + 2 * incoming * normal[0],
            velocity[1] + 2 * incoming * normal[1],
        )
        shift_i = target_key[1]
        shift_j = target_key[2]
        position = (
            impact[0] - shift_i,
            impact[1] - shift_j,
        )
        velocity = reflected
        cumulative_i += shift_i
        cumulative_j += shift_j
        cumulative_lifts.append((cumulative_i, cumulative_j))
        source_obstacle = module.obstacle(target_key[0], 0, 0)

    final_base = module.obstacle(word[-1][0], 0, 0)
    final_normal = (
        (position[0] - final_base.center[0]) / final_base.radius,
        (position[1] - final_base.center[1]) / final_base.radius,
    )
    final_theta = dual_atan2(module, final_normal[1], final_normal[0])
    final_tangent = -final_normal[1], final_normal[0]
    final_momentum = module.dual_dot(velocity, final_tangent)
    return PathResult(
        final_theta,
        final_momentum,
        minima,
        tuple(cumulative_lifts),
    )


def setup_fixed_data(module):
    frozen_root = module.certify_orbit_root()
    # The frozen 1e-50 box is deliberately much wider than needed for the
    # periodic root.  A local interval-Newton step sharpens it before the
    # 10^8-expanding reverse connector path is evaluated.
    refined_radius = "1e-70"
    refined_boxes = [module.arb(value, refined_radius) for value in module.ROOT_CENTERS]
    values, _ = module.half_orbit_equations(frozen_root.centers, True)
    _, jacobian_box = module.half_orbit_equations(refined_boxes, True)
    center_vector = module.arb_mat([[value] for value in frozen_root.centers])
    value_vector = module.arb_mat([[value] for value in values])
    interval_newton = center_vector - module.arb_mat(jacobian_box).inv() * value_vector
    if not all(
        refined_boxes[index].contains_interior(interval_newton[index, 0])
        for index in range(len(refined_boxes))
    ):
        raise RuntimeError("refined connector interval-Newton inclusion failed")
    refined_determinant = module.arb_mat(jacobian_box).det()
    if refined_determinant.contains(0):
        raise RuntimeError("refined connector Jacobian may be singular")
    root = module.RootCertificate(
        frozen_root.centers,
        refined_boxes,
        interval_newton,
        refined_determinant,
    )
    print("CONNECTOR_ROOT_REFINEMENT: CERTIFIED")
    print(f"  refined_root_box_radius={refined_radius}")
    sqrt_two = module.arb(2).sqrt()
    beta_a = (module.arb(859) - 550 * sqrt_two) / 100
    gamma_a = module.arb(625) * (25 - 4 * sqrt_two) / 324
    slope_a = (gamma_a / beta_a).sqrt()
    matrix_b, angle_residual, momentum_residual = module.connector_derivative(root.boxes[0])
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("connector root does not close in its certified box")
    slope_b = (matrix_b[1, 0] / matrix_b[0, 1]).sqrt()
    return root, slope_a, slope_b


def equations(module, root, slope_a, slope_b, t_box, u_box):
    dimension = 2
    t = module.Dual(t_box, [module.arb(1), module.arb(0)])
    u = module.Dual(u_box, [module.arb(0), module.arb(1)])
    qnl_theta = module.Dual(module.arb.pi() / 4, dimension=dimension) + t / module.R_GRAY
    qnl_momentum = slope_a * t
    qnl_result = propagate(
        module, "G", qnl_theta, qnl_momentum, QNL_FORWARD_WORD
    )

    connector_theta = module.Dual(root.boxes[0], dimension=dimension) + u / module.R_GRAY
    connector_momentum = -slope_b * u
    # T^{-14}=I T^{14} I.  Flip momentum before the declared forward word,
    # then flip the terminal momentum once more.
    connector_result = propagate(
        module,
        "G",
        connector_theta,
        -connector_momentum,
        CONNECTOR_REVERSE_FORWARD_WORD,
    )
    connector_result.momentum = -connector_result.momentum

    residuals = (
        qnl_result.theta - connector_result.theta,
        qnl_result.momentum - connector_result.momentum,
    )
    values = [entry.value for entry in residuals]
    jacobian = [entry.derivative for entry in residuals]
    return values, jacobian, qnl_result, connector_result


def forward_transition_coordinates(module, root, slope_a, slope_b, a_box, b_box):
    """Return connector eigen-coordinates after the 24-collision word."""

    dimension = 2
    a = module.Dual(a_box, [module.arb(1), module.arb(0)])
    b = module.Dual(b_box, [module.arb(0), module.arb(1)])
    theta = module.Dual(module.arb.pi() / 4, dimension=dimension) + (a + b) / module.R_GRAY
    momentum = slope_a * (a - b)
    result = propagate(
        module, "G", theta, momentum, FULL_FORWARD_TRANSITION_WORD
    )
    delta_s = module.R_GRAY * (
        result.theta - module.Dual(root.boxes[0], dimension=dimension)
    )
    unstable = (delta_s + result.momentum / slope_b) / 2
    stable = (delta_s - result.momentum / slope_b) / 2
    return unstable, stable, result


def midpoint_decimal(value, digits: int = 105) -> str:
    return value.str(digits, radius=False, more=True)


def refine_center(module, root, slope_a, slope_b):
    t_decimal = T_SEED
    u_decimal = U_SEED
    for _ in range(7):
        values, jacobian, _, _ = equations(
            module,
            root,
            slope_a,
            slope_b,
            module.arb(t_decimal),
            module.arb(u_decimal),
        )
        correction = module.arb_mat(jacobian).inv() * module.arb_mat(
            [[values[0]], [values[1]]]
        )
        t_new = module.arb(t_decimal) - correction[0, 0]
        u_new = module.arb(u_decimal) - correction[1, 0]
        t_decimal = midpoint_decimal(t_new)
        u_decimal = midpoint_decimal(u_new)
    return t_decimal, u_decimal


def rational_preconditioner(module, jacobian):
    inverse = module.arb_mat(jacobian).inv()
    rows = []
    for row in range(2):
        entries = []
        for column in range(2):
            decimal = midpoint_decimal(inverse[row, column], PRECONDITIONER_DIGITS)
            rational = Fraction(decimal)
            entries.append(
                module.arb(module.fmpq(rational.numerator, rational.denominator))
            )
        rows.append(entries)
    return module.arb_mat(rows)


def certify_root(module, root, slope_a, slope_b):
    t_decimal, u_decimal = refine_center(module, root, slope_a, slope_b)
    t_center = module.arb(t_decimal)
    u_center = module.arb(u_decimal)

    # The unequal radii reflect the 10^5 versus 10^8 endpoint expansions.
    t_radius = "1e-43"
    u_radius = "1e-46"
    t_box = module.arb(t_decimal, t_radius)
    u_box = module.arb(u_decimal, u_radius)
    center_values, center_jacobian, _, _ = equations(
        module, root, slope_a, slope_b, t_center, u_center
    )
    _, box_jacobian, qnl_result, connector_result = equations(
        module, root, slope_a, slope_b, t_box, u_box
    )
    preconditioner = rational_preconditioner(module, center_jacobian)
    identity = module.arb_mat([[1, 0], [0, 1]])
    center_vector = module.arb_mat([[t_center], [u_center]])
    residual_vector = module.arb_mat([[center_values[0]], [center_values[1]]])
    centered_box = module.arb_mat(
        [[module.arb(0, t_radius)], [module.arb(0, u_radius)]]
    )
    krawczyk = (
        center_vector
        - preconditioner * residual_vector
        + (identity - preconditioner * module.arb_mat(box_jacobian)) * centered_box
    )
    print(f"  diagnostic_center_residual={center_values}")
    print(f"  diagnostic_center_jacobian={module.arb_mat(center_jacobian)}")
    print(f"  diagnostic_box_jacobian={module.arb_mat(box_jacobian)}")
    print(f"  diagnostic_krawczyk={krawczyk}")
    if not t_box.contains_interior(krawczyk[0, 0]):
        raise RuntimeError(f"t Krawczyk inclusion fails: X={t_box}, K={krawczyk[0,0]}")
    if not u_box.contains_interior(krawczyk[1, 0]):
        raise RuntimeError(f"u Krawczyk inclusion fails: X={u_box}, K={krawczyk[1,0]}")

    jacobian_determinant = module.arb_mat(box_jacobian).det()
    if jacobian_determinant.contains(0):
        raise RuntimeError(f"matching Jacobian may vanish: {jacobian_determinant}")

    forward_unstable, forward_stable, _ = forward_transition_coordinates(
        module, root, slope_a, slope_b, t_box, module.arb(0)
    )
    if not forward_unstable.value.contains(0):
        raise RuntimeError(
            f"forward transition misses connector stable axis: {forward_unstable.value}"
        )
    if not forward_stable.value.contains(u_box):
        raise RuntimeError(
            f"forward transition stable coordinate misses matching root: "
            f"{forward_stable.value} versus {u_box}"
        )

    minima = {}
    for name in ("flight", "discriminant", "incidence", "clearance"):
        left = qnl_result.minima[name]
        right = connector_result.minima[name]
        if left is None or right is None:
            raise RuntimeError(f"missing physical minimum {name}")
        minima[name] = left.min(right)
    thresholds = {
        "flight": module.arb(1) / 10,
        "discriminant": module.arb(1) / 100,
        "incidence": module.arb(1) / 2,
        "clearance": module.arb(1) / 10,
    }
    for name, threshold in thresholds.items():
        if not minima[name] > threshold:
            raise RuntimeError(
                f"physical margin {name} does not exceed {threshold}: {minima[name]}"
            )

    print("TANGENT_LINE_MATCHING_ROOT: CERTIFIED")
    print(f"  arb_precision_bits={module.ctx.prec}")
    print(f"  t_qnl_unstable={t_box}")
    print(f"  u_connector_stable={u_box}")
    print(f"  tangent_matching_jacobian_determinant={jacobian_determinant}")
    print(
        "  finite_word_tangent_coordinate_jacobian="
        f"{module.arb_mat([forward_unstable.derivative, forward_stable.derivative])}"
    )
    print(f"  qnl_forward_word={QNL_FORWARD_WORD}")
    print(f"  connector_reverse_forward_word={CONNECTOR_REVERSE_FORWARD_WORD}")
    print(f"  qnl_cumulative_lifts={qnl_result.cumulative_lifts}")
    print(f"  connector_cumulative_lifts={connector_result.cumulative_lifts}")
    for name, value in minima.items():
        print(f"  minimum_{name}={value}")
    print("  transparent_wall_crossings=0")
    print("  finite_lattice_exhaustion=[-3,3]^2; omitted_coordinate_gap>=2")
    return t_box, u_box, jacobian_determinant


def main() -> int:
    module = load_frozen_certificate()
    try:
        root, slope_a, slope_b = setup_fixed_data(module)
        print(f"  diagnostic_slope_a={slope_a}")
        print(f"  diagnostic_slope_b={slope_b}")
        certify_root(module, root, slope_a, slope_b)
    except Exception as exc:
        print(f"TANGENT_LINE_MATCHING_ROOT: FAILED: {exc}")
        print("FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED")
        print("TRANSPORTED_TWISTING: NOT CERTIFIED")
        return 1
    print("TANGENT_LINE_MATCHING_SEED: CERTIFIED")
    print("  warning=eigentangents are not invariant-manifold graphs")
    print("HETEROCLINIC_INTERSECTION: NOT CERTIFIED")
    print("MICRO_FULL_CROSS_TRANSITION: NOT CERTIFIED")
    print("  reason=no invariant-graph/remainder enclosure and direct 24-step wrapping")
    print("FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED")
    print("  missing=validated invariant graphs, rectangle widths, and four face inequalities")
    print("TRANSPORTED_TWISTING: NOT CERTIFIED")
    print("  missing=loop derivative on the closed common-vertex word")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
