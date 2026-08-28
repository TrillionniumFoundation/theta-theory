#!/usr/bin/env python3
"""Certify one nonlinear connector shooting tile by interval Newton.

In the connector eigen-coordinates

    (s,p) = a (1,k) + b (1,-k),

fix ``b=h/2``, where ``h`` is half the connector--QNL center separation.
For the complete period-eight connector word, let ``A(a)`` be the unstable
coordinate of the image.  This certificate proves that ``A(a)=0`` has one
and only one solution in an explicit interval.  Thus the straight choice
``a=0`` has a rigorously nonzero nonlinear correction at this transverse
slice.

This is only a finite-time preimage of the *center stable tangent*.  It is
not, by itself, a stable-manifold or full-cross Markov-strip certificate.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


FROZEN_CERT = Path(__file__).with_name("cm2_fixed_section_common_vertex_cert.py")


def load_frozen_certificate():
    spec = importlib.util.spec_from_file_location("cm2_v52_common_vertex", FROZEN_CERT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load frozen certificate {FROZEN_CERT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def dot(left, right):
    return left[0] * right[0] + left[1] * right[1]


def same_obstacle(left, right):
    return (left.kind, left.i, left.j) == (right.kind, right.i, right.j)


def segment_distance_squared(source, target, center):
    direction = target[0] - source[0], target[1] - source[1]
    source_to_center = center[0] - source[0], center[1] - source[1]
    denominator = dot(direction, direction)
    projection = dot(source_to_center, direction) / denominator
    if projection < 0:
        return dot(source_to_center, source_to_center)
    if projection > 1:
        target_to_center = center[0] - target[0], center[1] - target[1]
        return dot(target_to_center, target_to_center)
    projected = dot(source_to_center, direction)
    return dot(source_to_center, source_to_center) - projected * projected / denominator


def ray_circle(position, velocity, target):
    displacement = position[0] - target.center[0], position[1] - target.center[1]
    linear = dot(displacement, velocity)
    offset = dot(displacement, displacement) - target.radius * target.radius
    discriminant = linear * linear - offset
    if not discriminant > 0:
        raise RuntimeError(f"target discriminant is not positive: {discriminant}")
    flight = -linear - discriminant.sqrt()
    if not flight > 0:
        raise RuntimeError(f"near collision root is not forward: {flight}")
    impact = position[0] + flight * velocity[0], position[1] + flight * velocity[1]
    normal = (
        (impact[0] - target.center[0]) / target.radius,
        (impact[1] - target.center[1]) / target.radius,
    )
    arrival = -dot(velocity, normal)
    if not arrival > 0:
        raise RuntimeError(f"target arrival is not transverse: {arrival}")
    reflected = (
        velocity[0] + 2 * arrival * normal[0],
        velocity[1] + 2 * arrival * normal[1],
    )
    return impact, reflected, flight, discriminant, arrival


def certify_segment_clearance(module, source, target, source_obstacle, target_obstacle):
    minimum = None
    for candidate in module.all_lattice_obstacles():
        if same_obstacle(candidate, source_obstacle) or same_obstacle(candidate, target_obstacle):
            continue
        distance_squared = segment_distance_squared(source, target, candidate.center)
        if not distance_squared > candidate.radius * candidate.radius:
            raise RuntimeError(
                "unintended obstacle may meet segment against "
                f"{(candidate.kind, candidate.i, candidate.j)}: {distance_squared}"
            )
        clearance = distance_squared.sqrt() - candidate.radius
        minimum = clearance if minimum is None else minimum.min(clearance)
    if minimum is None:
        raise RuntimeError("empty finite-lattice clearance enumeration")
    return minimum


def return_unstable(module, base_angle, slope, a, b):
    """Return A(a) and dA/da through the declared connector word."""

    coordinate = module.Dual(a, [module.arb(1)])
    stable_coordinate = module.Dual(b, [module.arb(0)])
    arclength = coordinate + stable_coordinate
    momentum = slope * (coordinate - stable_coordinate)
    theta = module.Dual(base_angle, [module.arb(0)]) + arclength / module.R_GRAY
    normal = module.dual_cos(theta), module.dual_sin(theta)
    tangent = -normal[1], normal[0]
    cosine_phi = module.dual_sqrt(1 - momentum * momentum)
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    first = module.FULL_OBSTACLES[0]
    position = (
        first.center[0] + first.radius * normal[0],
        first.center[1] + first.radius * normal[1],
    )
    for target in module.FULL_OBSTACLES[1:] + module.FULL_OBSTACLES[:1]:
        position, velocity = module.ray_circle_collision(position, velocity, target)

    final_normal = (
        (position[0] - first.center[0]) / first.radius,
        (position[1] - first.center[1]) / first.radius,
    )
    final_tangent = -final_normal[1], final_normal[0]
    final_angle = module.arb.atan2(final_normal[1].value, final_normal[0].value)
    angle_derivative = (
        final_normal[0].value * final_normal[1].derivative[0]
        - final_normal[1].value * final_normal[0].derivative[0]
    )
    final_momentum = module.dual_dot(velocity, final_tangent)
    final_arclength = module.R_GRAY * (final_angle - base_angle)
    final_arclength_derivative = module.R_GRAY * angle_derivative
    value = (final_arclength + final_momentum.value / slope) / 2
    derivative = (final_arclength_derivative + final_momentum.derivative[0] / slope) / 2
    return value, derivative


def certify_physical_tube(module, base_angle, slope, a_box, b):
    source_arclength = a_box + b
    source_momentum = slope * (a_box - b)
    source_angle = base_angle + source_arclength / module.R_GRAY
    normal = source_angle.cos(), source_angle.sin()
    tangent = -normal[1], normal[0]
    cosine_phi = (1 - source_momentum * source_momentum).sqrt()
    velocity = (
        cosine_phi * normal[0] + source_momentum * tangent[0],
        cosine_phi * normal[1] + source_momentum * tangent[1],
    )
    gray = module.FULL_OBSTACLES[0]
    position = (
        gray.center[0] + gray.radius * normal[0],
        gray.center[1] + gray.radius * normal[1],
    )

    minimum_flight = None
    minimum_discriminant = None
    minimum_incidence = None
    minimum_clearance = None
    source_obstacle = gray
    module.certify_lattice_exhaustion(module.arb("0.15"))
    for index, target_obstacle in enumerate(
        module.FULL_OBSTACLES[1:] + module.FULL_OBSTACLES[:1], start=1
    ):
        impact, reflected, flight, discriminant, incidence = ray_circle(
            position, velocity, target_obstacle
        )
        clearance = certify_segment_clearance(
            module, position, impact, source_obstacle, target_obstacle
        )
        for label, point in (("source", position), ("impact", impact)):
            if not (point[0] > 0 and point[0] < 1 and point[1] > 0 and point[1] < 1):
                raise RuntimeError(
                    f"transparent-wall crossing possible at segment {index} {label}: {point}"
                )
        minimum_flight = flight if minimum_flight is None else minimum_flight.min(flight)
        minimum_discriminant = discriminant if minimum_discriminant is None else minimum_discriminant.min(discriminant)
        minimum_incidence = incidence if minimum_incidence is None else minimum_incidence.min(incidence)
        minimum_clearance = clearance if minimum_clearance is None else minimum_clearance.min(clearance)
        position, velocity, source_obstacle = impact, reflected, target_obstacle

    if not minimum_flight > module.arb("0.1"):
        raise RuntimeError(f"flight margin <=0.1: {minimum_flight}")
    if not minimum_discriminant > module.arb("0.01"):
        raise RuntimeError(f"discriminant margin <=0.01: {minimum_discriminant}")
    if not minimum_incidence > module.arb("0.5"):
        raise RuntimeError(f"incidence margin <=0.5: {minimum_incidence}")
    if not minimum_clearance > module.arb("0.15"):
        raise RuntimeError(f"unintended clearance margin <=0.15: {minimum_clearance}")
    return (
        source_angle,
        source_momentum,
        minimum_flight,
        minimum_discriminant,
        minimum_incidence,
        minimum_clearance,
    )


def main() -> None:
    module = load_frozen_certificate()
    root = module.certify_orbit_root()
    matrix, angle_residual, momentum_residual = module.connector_derivative(root.boxes[0])
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("certified connector center does not close")
    eigen_slope = (matrix[1, 0] / matrix[0, 1]).sqrt()
    # Use a fixed rational chart slope.  Keeping an interval-valued slope in
    # every iterate creates a dependency blow-up unrelated to the scalar
    # shooting variable.  The inclusion below proves that this exact decimal
    # rational lies on the certified center eigen-slope ball.
    slope = module.arb(
        "6.779460879726527387379610900452463910239929566858300414751989924810597"
    )
    if not eigen_slope.contains(slope):
        raise RuntimeError(f"rational chart slope misses eigen-slope ball: {eigen_slope}")
    # Likewise freeze the displayed rational center of the Krawczyk box as
    # the chart origin; the true connector angle remains within 1e-50.
    base_angle = module.arb(module.ROOT_CENTERS[0])
    if not root.boxes[0].contains(base_angle):
        raise RuntimeError("rational chart origin misses connector root box")
    center_gap = module.R_GRAY * (module.arb.pi() / 4 - base_angle)
    half_side = center_gap / 2
    b = half_side / 2

    # Fixed exact decimal interval for a scalar interval-Newton proof.
    center_string = "-6.03958742449805675289833564104322857383918327337e-12"
    center = module.arb(center_string)
    domain = module.arb(center_string, "1e-25")
    center_value, _ = return_unstable(module, base_angle, slope, center, b)
    _, derivative_box = return_unstable(module, base_angle, slope, domain, b)
    if derivative_box.contains(0) or not derivative_box > module.arb(100_000_000):
        raise RuntimeError(f"shooting derivative lacks transversality: {derivative_box}")
    newton_image = center - center_value / derivative_box
    if not domain.contains_interior(newton_image):
        raise RuntimeError(
            f"interval Newton image is not in the interior: X={domain}, N={newton_image}"
        )
    if not domain < 0 or not abs(domain) > module.arb("5e-12"):
        raise RuntimeError(f"nonlinear source correction is not separated from zero: {domain}")

    physical = certify_physical_tube(module, base_angle, slope, domain, b)
    source_angle, source_momentum, min_flight, min_disc, min_inc, min_clear = physical

    print("CONNECTOR_STABLE_TANGENT_SHOOTING_TILE: CERTIFIED")
    print("  equation=A_8(a,b=h/2)=0")
    print(f"  connector_eigen_slope_ball={eigen_slope}")
    print(f"  rational_chart_slope_k={slope}")
    print(f"  center_gap={center_gap}")
    print(f"  product_hull_side_h={half_side}")
    print(f"  fixed_stable_coordinate_b={b}")
    print(f"  source_unstable_domain_X={domain}")
    print(f"  center_residual_A8={center_value}")
    print(f"  derivative_dA8_da_on_X={derivative_box}")
    print(f"  interval_newton_image={newton_image}")
    print("  unique_root_in_X=yes")
    print("  nonlinear_correction=a_root< -5e-12")
    print(f"  source_angle_tube={source_angle}")
    print(f"  source_momentum_tube={source_momentum}")
    print("  physical_word=14 collisions / 8 fixed-section returns")
    print(f"  minimum_flight={min_flight}")
    print(f"  minimum_target_discriminant={min_disc}")
    print(f"  minimum_incidence_cosine={min_inc}")
    print(f"  minimum_unintended_obstacle_clearance={min_clear}")
    print("  transparent_wall_crossings=0")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=stable-manifold graph continuation and full-cross inequalities")


if __name__ == "__main__":
    main()
