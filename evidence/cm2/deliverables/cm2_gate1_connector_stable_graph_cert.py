#!/usr/bin/env python3
"""Validated connector invariant graphs by recentered collision jets.

Raw interval propagation through the fourteen-collision connector word loses
the shooting-parameter correlation.  This certificate instead evaluates a
fresh local second-order jet at each certified collision box, propagates the
reachable radius with the mean-value theorem, and composes the Jacobian and
Hessian tensors separately.  A graph-transform audit is then performed only
on the small preimage core needed to cover the requested graph domain.

The connector word is palindromic about its zero-momentum gray base point.
After validating the unstable graph, exact billiard reversibility maps it to
the stable graph used by the Gate 1 shooting problem.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path


QNL_GRAPH_CERT = Path(__file__).with_name("cm2_gate1_qnl_unstable_graph_cert.py")
TANGENT_CERT = Path(__file__).with_name("cm2_gate1_tangent_line_matching_cert.py")
PRECISION_BITS = 400

TARGET_RADIUS = "3e-12"
PREIMAGE_CORE_RADIUS = "4e-20"
QUADRATIC_CONSTANT = "1e-2"
LIPSCHITZ_CONSTANT = "1e-8"
SHOOTING_U = "2.186137101021440040809485447235071e-12"


def load_helper(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load helper {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def zero_ball(module, radius):
    """Return a symmetric Arb ball rigorously containing +/- ``radius``."""

    inflated = 4 * abs(radius)
    text = inflated.str(110, radius=False, more=True)
    result = module.arb(0, text)
    if not result.contains(radius) or not result.contains(-radius):
        raise RuntimeError(f"failed to inflate reachable radius {radius}")
    return result


def matrix_product(module, left, right):
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(2)),
                module.arb(0),
            )
            for j in range(2)
        ]
        for i in range(2)
    ]


@dataclass
class StepData:
    angle: object
    momentum: object
    position: tuple[object, object]
    impact: tuple[object, object]
    flight: object
    discriminant: object
    incidence: object
    clearance: object


def same_obstacle(left, right) -> bool:
    return (left.kind, left.i, left.j) == (right.kind, right.i, right.j)


def segment_clearance(module, source, target, source_obstacle, target_obstacle):
    minimum = None
    for candidate in module.all_lattice_obstacles():
        if same_obstacle(candidate, source_obstacle) or same_obstacle(
            candidate, target_obstacle
        ):
            continue
        distance_squared = module.minimum_line_segment_distance_squared(
            source, target, candidate.center
        )
        if not distance_squared > candidate.radius * candidate.radius:
            raise RuntimeError(
                "connector core may hit an undeclared lift: "
                f"{(candidate.kind, candidate.i, candidate.j)}"
            )
        value = distance_squared.sqrt() - candidate.radius
        minimum = value if minimum is None else minimum.min(value)
    if minimum is None:
        raise RuntimeError("empty connector clearance enumeration")
    return minimum


def collision_step(qnl, module, source, target, angle_box, momentum_box) -> StepData:
    Jet2 = qnl.Jet2
    theta = Jet2.variable(module, angle_box, 0)
    momentum = Jet2.variable(module, momentum_box, 1)
    normal = theta.cos(), theta.sin()
    tangent = -normal[1], normal[0]
    cosine_phi = (1 - momentum * momentum).sqrt()
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    position = (
        source.center[0] + source.radius * normal[0],
        source.center[1] + source.radius * normal[1],
    )
    displacement = (
        position[0] - target.center[0],
        position[1] - target.center[1],
    )
    linear = qnl.jet_dot(displacement, velocity)
    offset = qnl.jet_dot(displacement, displacement) - target.radius**2
    discriminant = linear * linear - offset
    if not discriminant.value > 0:
        raise RuntimeError(f"connector discriminant may vanish: {discriminant.value}")
    flight = -linear - discriminant.sqrt()
    if not flight.value > 0:
        raise RuntimeError(f"connector flight may be nonpositive: {flight.value}")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    target_normal = (
        (impact[0] - target.center[0]) / target.radius,
        (impact[1] - target.center[1]) / target.radius,
    )
    incidence = -qnl.jet_dot(velocity, target_normal)
    if not incidence.value > 0:
        raise RuntimeError(f"connector incidence may vanish: {incidence.value}")
    reflected = (
        velocity[0] + 2 * incidence * target_normal[0],
        velocity[1] + 2 * incidence * target_normal[1],
    )
    output_angle = qnl.jet_atan2(module, target_normal[1], target_normal[0])
    output_tangent = -target_normal[1], target_normal[0]
    output_momentum = qnl.jet_dot(reflected, output_tangent)

    source_value = position[0].value, position[1].value
    target_value = impact[0].value, impact[1].value
    for endpoint in (source_value, target_value):
        for coordinate in endpoint:
            if not coordinate > module.arb(1) / 25 or not coordinate < module.arb(4) / 5:
                raise RuntimeError(
                    f"connector core endpoint leaves (1/25,4/5)^2: {coordinate}"
                )
    clearance = segment_clearance(
        module, source_value, target_value, source, target
    )
    return StepData(
        output_angle,
        output_momentum,
        source_value,
        target_value,
        flight.value,
        discriminant.value,
        incidence.value,
        clearance,
    )


@dataclass
class ReturnJet:
    jacobian: list[list[object]]
    hessians: list[list[list[object]]]
    minimum_flight: object
    minimum_discriminant: object
    minimum_incidence: object
    minimum_clearance: object
    final_angle_deviation: object
    final_momentum_deviation: object


def compose_connector_core(qnl, module, root, slope, rho, c) -> ReturnJet:
    obstacles = list(module.FULL_OBSTACLES)
    angles = root.boxes + list(reversed(root.boxes[1:-1]))
    points, normals = module.collision_points(angles, obstacles)
    nominal_momenta = []
    for index in range(len(obstacles)):
        velocity = module.arb_unit(points[index], points[(index + 1) % len(points)])
        tangent = -normals[index][1], normals[index][0]
        nominal_momenta.append(module.arb_dot(velocity, tangent))

    if not nominal_momenta[0].contains(0):
        raise RuntimeError("connector base momentum is not fixed by time reversal")
    if module.FULL_KEYS[1:] != tuple(reversed(module.FULL_KEYS[1:])):
        raise RuntimeError("connector target word is not palindromic")

    ordinate_radius = c * rho * rho
    angle_deviation = (rho + ordinate_radius) / module.R_GRAY
    momentum_deviation = slope * (rho + ordinate_radius)
    jacobian = [
        [module.arb(1), module.arb(0)],
        [module.arb(0), module.arb(1)],
    ]
    hessians = [
        [[module.arb(0), module.arb(0)], [module.arb(0), module.arb(0)]],
        [[module.arb(0), module.arb(0)], [module.arb(0), module.arb(0)]],
    ]
    minima = {"flight": None, "discriminant": None, "incidence": None, "clearance": None}

    for index, source in enumerate(obstacles):
        target = obstacles[(index + 1) % len(obstacles)]
        angle_box = angles[index] + zero_ball(module, angle_deviation)
        momentum_box = nominal_momenta[index] + zero_ball(
            module, momentum_deviation
        )
        step = collision_step(qnl, module, source, target, angle_box, momentum_box)
        step_jacobian = [step.angle.gradient, step.momentum.gradient]
        step_hessians = [step.angle.hessian, step.momentum.hessian]

        next_jacobian = matrix_product(module, step_jacobian, jacobian)
        next_hessians = []
        for output in range(2):
            tensor = [[module.arb(0) for _ in range(2)] for _ in range(2)]
            for left in range(2):
                for right in range(2):
                    tensor[left][right] = sum(
                        (
                            step_jacobian[output][middle]
                            * hessians[middle][left][right]
                            for middle in range(2)
                        ),
                        module.arb(0),
                    ) + sum(
                        (
                            step_hessians[output][first][second]
                            * jacobian[first][left]
                            * jacobian[second][right]
                            for first in range(2)
                            for second in range(2)
                        ),
                        module.arb(0),
                    )
            next_hessians.append(tensor)

        next_angle_deviation = (
            abs(step_jacobian[0][0]) * angle_deviation
            + abs(step_jacobian[0][1]) * momentum_deviation
        )
        next_momentum_deviation = (
            abs(step_jacobian[1][0]) * angle_deviation
            + abs(step_jacobian[1][1]) * momentum_deviation
        )
        jacobian = next_jacobian
        hessians = next_hessians
        angle_deviation = next_angle_deviation
        momentum_deviation = next_momentum_deviation

        for name, value in (
            ("flight", step.flight),
            ("discriminant", step.discriminant),
            ("incidence", step.incidence),
            ("clearance", step.clearance),
        ):
            minima[name] = value if minima[name] is None else minima[name].min(value)

    # Linear input/output coordinate changes between (theta,p) and (x,y).
    input_change = [
        [1 / module.R_GRAY, 1 / module.R_GRAY],
        [slope, -slope],
    ]
    output_change = [
        [module.R_GRAY / 2, 1 / (2 * slope)],
        [module.R_GRAY / 2, -1 / (2 * slope)],
    ]
    eigen_jacobian = matrix_product(
        module, matrix_product(module, output_change, jacobian), input_change
    )
    eigen_hessians = []
    for output in range(2):
        tensor = [[module.arb(0) for _ in range(2)] for _ in range(2)]
        for left in range(2):
            for right in range(2):
                tensor[left][right] = sum(
                    (
                        output_change[output][physical_output]
                        * hessians[physical_output][first][second]
                        * input_change[first][left]
                        * input_change[second][right]
                        for physical_output in range(2)
                        for first in range(2)
                        for second in range(2)
                    ),
                    module.arb(0),
                )
        eigen_hessians.append(tensor)

    return ReturnJet(
        eigen_jacobian,
        eigen_hessians,
        minima["flight"],
        minima["discriminant"],
        minima["incidence"],
        minima["clearance"],
        angle_deviation,
        momentum_deviation,
    )


def certify_connector_graph():
    qnl = load_helper(QNL_GRAPH_CERT, "cm2_gate1_qnl_graph_helper")
    tangent = load_helper(TANGENT_CERT, "cm2_gate1_tangent_helper")
    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    root, _, slope = tangent.setup_fixed_data(module)
    matrix, angle_residual, momentum_residual = module.connector_derivative(
        root.boxes[0]
    )
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("refined connector center does not close")

    target_radius = module.arb(TARGET_RADIUS)
    rho = module.arb(PREIMAGE_CORE_RADIUS)
    c = module.arb(QUADRATIC_CONSTANT)
    lipschitz = module.arb(LIPSCHITZ_CONSTANT)
    data = compose_connector_core(qnl, module, root, slope, rho, c)
    a_x, a_y = data.jacobian[0]
    b_x, b_y = data.jacobian[1]
    raw_interval_determinant = a_x * b_y - a_y * b_x
    m_a = a_x - abs(a_y) * lipschitz
    coverage = m_a * rho
    image_lipschitz = (abs(b_x) + abs(b_y) * lipschitz) / m_a
    contraction = abs(b_y) + (
        abs(b_x) + lipschitz * abs(b_y)
    ) * abs(a_y) / m_a

    hessian = data.hessians[1]
    quadratic_remainder = (
        abs(hessian[0][0])
        + 2 * abs(hessian[0][1]) * c * rho
        + abs(hessian[1][1]) * c * c * rho * rho
    ) / 2
    eigen_root = (matrix[0, 1] * matrix[1, 0]).sqrt()
    unstable_multiplier = matrix[0, 0] + eigen_root
    stable_multiplier = matrix[0, 0] - eigen_root
    quadratic_image = (
        abs(stable_multiplier) * c + quadratic_remainder
    ) / (m_a * m_a)

    if not data.jacobian[0][0].contains(unstable_multiplier):
        raise RuntimeError("composed connector jet misses frozen unstable multiplier")
    if not data.jacobian[1][1].contains(stable_multiplier):
        raise RuntimeError("composed connector jet misses frozen stable multiplier")
    # In arclength--momentum coordinates every regular billiard collision
    # preserves ds wedge dp exactly.  The fourteen-step return and the two
    # reciprocal linear eigen-coordinate changes therefore have determinant
    # exactly one.  A direct determinant of the wide interval matrix loses
    # this correlation and is retained only as a wrapping diagnostic.
    if not (
        matrix.det() > module.arb(999) / 1000
        and matrix.det() < module.arb(1001) / 1000
    ):
        raise RuntimeError("frozen connector derivative is not symplectic")
    if not (matrix[0, 0] - matrix[1, 1]).contains(0):
        raise RuntimeError("connector reversibility diagonal identity fails")
    if not coverage > target_radius:
        raise RuntimeError(
            f"connector preimage core does not cover graph domain: {coverage}"
        )
    if not image_lipschitz < lipschitz:
        raise RuntimeError(
            f"connector derivative cone is not invariant: {image_lipschitz}"
        )
    if not contraction < 1:
        raise RuntimeError(f"connector graph transform is not contractive: {contraction}")
    if not quadratic_image < c:
        raise RuntimeError(
            f"connector quadratic tube is not invariant: {quadratic_image}"
        )
    if not module.arb(3) - module.R_GRAY > 2:
        raise RuntimeError("connector omitted-lift exhaustion inequality failed")
    thresholds = {
        "flight": module.arb(1) / 10,
        "discriminant": module.arb(1) / 1000,
        "incidence": module.arb(1) / 2,
        "clearance": module.arb(1) / 10,
    }
    physical = {
        "flight": data.minimum_flight,
        "discriminant": data.minimum_discriminant,
        "incidence": data.minimum_incidence,
        "clearance": data.minimum_clearance,
    }
    for name, threshold in thresholds.items():
        if not physical[name] > threshold:
            raise RuntimeError(f"connector core physical margin {name} fails: {physical[name]}")

    shooting_u = module.arb(SHOOTING_U)
    if not abs(shooting_u) < target_radius:
        raise RuntimeError("connector shooting parameter leaves stable graph domain")
    shooting_correction = c * shooting_u * shooting_u

    # The inverse stable leg is I*T^14*I.  Replay the entire validated stable
    # graph ordinate tube, not merely its affine tangent point.
    u_dual = module.Dual(shooting_u, dimension=0)
    h_tube = module.arb(
        0, shooting_correction.str(100, radius=False, more=True)
    )
    h_dual = module.Dual(h_tube, dimension=0)
    replay_theta = module.Dual(root.boxes[0], dimension=0) + (
        u_dual + h_dual
    ) / module.R_GRAY
    replay_momentum = slope * (u_dual - h_dual)
    replay = tangent.propagate(
        module,
        "G",
        replay_theta,
        replay_momentum,
        tangent.CONNECTOR_REVERSE_FORWARD_WORD,
    )
    replay.momentum = -replay.momentum
    for name, threshold in thresholds.items():
        if not replay.minima[name] > threshold:
            raise RuntimeError(
                f"connector stable graph-tube replay margin {name} fails: "
                f"{replay.minima[name]}"
            )

    print("CONNECTOR_LOCAL_UNSTABLE_GRAPH: CERTIFIED")
    print(f"  target_graph_radius={target_radius}")
    print(f"  evaluated_preimage_core_radius={rho}")
    print(f"  quadratic_remainder_bound=|h(x)|<={c}*x^2")
    print(f"  derivative_cone_bound=|h'(x)|<={lipschitz}")
    print(f"  eigen_D_F_core={module.arb_mat(data.jacobian)}")
    print("  det_D_F_core=1 (exact ds-wedge-dp symplectic identity)")
    print(f"  raw_interval_determinant_diagnostic={raw_interval_determinant}")
    print(f"  unstable_projection_lower={m_a}")
    print(f"  graph_domain_coverage={coverage}")
    print(f"  graph_transform_lipschitz_image={image_lipschitz}")
    print(f"  graph_transform_contraction={contraction}")
    print(f"  graph_transform_quadratic_image={quadratic_image}")
    print(f"  stable_component_hessian={module.arb_mat(hessian)}")
    print(f"  final_recentered_angle_deviation={data.final_angle_deviation}")
    print(f"  final_recentered_momentum_deviation={data.final_momentum_deviation}")
    for name, value in physical.items():
        print(f"  minimum_{name}={value}")
    print("  solid_collision_count=14")
    print("  recentered_collision_boxes=14")
    print("CONNECTOR_LOCAL_STABLE_GRAPH: CERTIFIED")
    print("  mechanism=I*T^14*I=T^-14 and palindromic word at p=0")
    print(f"  stable_graph_form=x=h(y), |y|<={target_radius}")
    print(f"  shooting_u={shooting_u}")
    print(f"  shooting_unstable_correction_bound={shooting_correction}")
    print("CONNECTOR_GRAPH_TUBE_REVERSE_FOURTEEN_REPLAY: CERTIFIED")
    print(f"  graph_correction_tube={h_tube}")
    print(f"  terminal_theta_box={replay.theta.value}")
    print(f"  terminal_momentum_box={replay.momentum.value}")
    for name, value in replay.minima.items():
        print(f"  replay_minimum_{name}={value}")
    print(f"  replay_forward_word={tangent.CONNECTOR_REVERSE_FORWARD_WORD}")
    print("  mechanism=T^-14=I*T^14*I")
    print("  warning=terminal interval width is not a true-matching enclosure")
    return module, root, slope, c, target_radius


def main() -> int:
    try:
        certify_connector_graph()
    except Exception as exc:
        print(f"CONNECTOR_LOCAL_UNSTABLE_GRAPH: FAILED: {exc}")
        print("CONNECTOR_LOCAL_STABLE_GRAPH: NOT CERTIFIED")
        print("TRUE_HETEROCLINIC_MATCHING: NOT CERTIFIED")
        print("FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED")
        return 1
    print("CONNECTOR_EIGENTANGENT_UPGRADE: CERTIFIED")
    print("TRUE_HETEROCLINIC_MATCHING: NOT CERTIFIED")
    print("  missing=correlation-preserving 10+14 image matching and true Krawczyk")
    print("FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
