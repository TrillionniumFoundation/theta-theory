#!/usr/bin/env python3
"""Certify a one-point quadratic connector invariance equation.

In connector eigen-coordinates, fix ``b=h/2`` and impose the quadratic graph
``a=c*b^2`` at both source and image.  For one complete connector cycle, let
``(A(c), B(c))`` be the image coordinates.  This certificate applies interval
Newton to

    F(c) = A(c) - c B(c)^2.

The result is a genuine nonlinear invariance equation at one transverse
point.  It is not an invariant graph on a nondegenerate b-interval.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SHOOTING_CERT = HERE / "cm2_connector_stable_shooting_tile_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def quadratic_residual(module, base_angle, slope, coefficient, stable_coordinate):
    """Return F(c), F'(c), A(c), and B(c) for one connector cycle."""

    coefficient_dual = module.Dual(coefficient, [module.arb(1)])
    stable_dual = module.Dual(stable_coordinate, [module.arb(0)])
    unstable_dual = coefficient_dual * stable_dual * stable_dual
    arclength = unstable_dual + stable_dual
    momentum = slope * (unstable_dual - stable_dual)
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
    unstable_value = (final_arclength + final_momentum.value / slope) / 2
    unstable_derivative = (
        final_arclength_derivative + final_momentum.derivative[0] / slope
    ) / 2
    stable_value = (final_arclength - final_momentum.value / slope) / 2
    stable_derivative = (
        final_arclength_derivative - final_momentum.derivative[0] / slope
    ) / 2
    residual = unstable_value - coefficient * stable_value * stable_value
    residual_derivative = unstable_derivative - (
        stable_value * stable_value
        + 2 * coefficient * stable_value * stable_derivative
    )
    return residual, residual_derivative, unstable_value, stable_value


def main():
    shooting = load_module("cm2_quadratic_shooting", SHOOTING_CERT)
    module = shooting.load_frozen_certificate()
    root = module.certify_orbit_root()
    matrix, angle_residual, momentum_residual = module.connector_derivative(root.boxes[0])
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("connector center does not close")
    slope = module.arb(
        "6.779460879726527387379610900452463910239929566858300414751989924810597"
    )
    if not (matrix[1, 0] / matrix[0, 1]).sqrt().contains(slope):
        raise RuntimeError("fixed chart slope misses certified eigen-slope")
    base_angle = module.arb(module.ROOT_CENTERS[0])
    if not root.boxes[0].contains(base_angle):
        raise RuntimeError("fixed chart origin misses connector root")
    h = module.R_GRAY * (module.arb.pi() / 4 - base_angle) / 2
    b = h / 2

    initial_domain = module.arb("-0.00043741941966527186", "1e-18")
    domain = initial_domain
    center_value = None
    derivative = None
    for _ in range(4):
        center = module.arb(domain.mid())
        center_value, _, _, _ = quadratic_residual(
            module, base_angle, slope, center, b
        )
        _, derivative, _, _ = quadratic_residual(
            module, base_angle, slope, domain, b
        )
        if derivative.contains(0):
            raise RuntimeError(f"coefficient derivative contains zero: {derivative}")
        newton_image = center - center_value / derivative
        if not domain.contains_interior(newton_image):
            raise RuntimeError(f"Newton inclusion failed: X={domain}, N={newton_image}")
        domain = newton_image

    _, _, image_unstable, image_stable = quadratic_residual(
        module, base_angle, slope, newton_image, b
    )
    source_unstable = newton_image * b * b
    physical = shooting.certify_physical_tube(
        module, base_angle, slope, source_unstable, b
    )
    if not derivative > module.arb("1"):
        raise RuntimeError(f"quadratic residual lacks derivative margin: {derivative}")
    if not newton_image < module.arb("-0.0004"):
        raise RuntimeError(f"quadratic coefficient lacks signed separation: {newton_image}")

    print("CONNECTOR_QUADRATIC_POINT_INVARIANCE: CERTIFIED")
    print(f"  fixed_stable_coordinate_b={b}")
    print(f"  initial_coefficient_domain={initial_domain}")
    print(f"  residual_at_center={center_value}")
    print(f"  derivative_dF_dc={derivative}")
    print(f"  interval_newton_image={newton_image}")
    print("  unique_coefficient=yes")
    print(f"  source_unstable_coordinate={source_unstable}")
    print(f"  image_unstable_coordinate={image_unstable}")
    print(f"  image_stable_coordinate={image_stable}")
    print("  invariant_residual_at_unique_root=0 (by interval-Newton theorem)")
    print(f"  minimum_flight={physical[2]}")
    print(f"  minimum_target_discriminant={physical[3]}")
    print(f"  minimum_incidence_cosine={physical[4]}")
    print(f"  minimum_unintended_obstacle_clearance={physical[5]}")
    print("  transparent_wall_crossings=0")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=quadratic graph invariance on a nondegenerate b-tile")


if __name__ == "__main__":
    main()
