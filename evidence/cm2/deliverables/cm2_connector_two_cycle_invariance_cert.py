#!/usr/bin/env python3
"""Test the first nonlinear stable-graph invariance condition rigorously.

For fixed stable coordinate ``b=h/2`` in the connector eigen-chart, first
enclose the unique root of the one-cycle terminal stable-tangent equation.
Then recondition its image using the exact equation ``A_1=0`` and test whether
the next connector cycle remains on that tangent.  A nonzero second-cycle
unstable coordinate rigorously falsifies tangent invariance.

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


def return_unstable_cycles(module, base_angle, slope, a, b, cycles, differentiate="a"):
    """Return terminal unstable coordinate and d/da after full cycles."""

    if differentiate not in ("a", "b"):
        raise ValueError("differentiate must be 'a' or 'b'")
    coordinate = module.Dual(a, [module.arb(1 if differentiate == "a" else 0)])
    stable_coordinate = module.Dual(b, [module.arb(1 if differentiate == "b" else 0)])
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
    word = module.FULL_OBSTACLES[1:] + module.FULL_OBSTACLES[:1]
    for _ in range(cycles):
        for target in word:
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


def return_coordinates_one_cycle(module, base_angle, slope, a, b):
    """Return the two connector eigen-coordinates after one full cycle."""

    coordinate = module.Dual(a, [module.arb(0)])
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
    final_momentum = module.dual_dot(velocity, final_tangent).value
    final_arclength = module.R_GRAY * (final_angle - base_angle)
    unstable = (final_arclength + final_momentum / slope) / 2
    stable = (final_arclength - final_momentum / slope) / 2
    return unstable, stable


def interval_newton(module, function, center_string, radius_string):
    center = module.arb(center_string)
    domain = module.arb(center_string, radius_string)
    center_value, _ = function(center)
    _, derivative = function(domain)
    if derivative.contains(0):
        raise RuntimeError(f"derivative contains zero: {derivative}")
    image = center - center_value / derivative
    if not domain.contains_interior(image):
        raise RuntimeError(f"Newton inclusion failed: X={domain}, N={image}")
    return domain, center_value, derivative, image


def main():
    shooting = load_module("cm2_shooting", SHOOTING_CERT)
    module = shooting.load_frozen_certificate()
    root = module.certify_orbit_root()
    matrix, angle_residual, momentum_residual = module.connector_derivative(root.boxes[0])
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("connector center does not close")
    slope = module.arb(
        "6.779460879726527387379610900452463910239929566858300414751989924810597"
    )
    eigen_slope = (matrix[1, 0] / matrix[0, 1]).sqrt()
    if not eigen_slope.contains(slope):
        raise RuntimeError("fixed rational slope misses certified eigen-slope")
    base_angle = module.arb(module.ROOT_CENTERS[0])
    if not root.boxes[0].contains(base_angle):
        raise RuntimeError("fixed rational origin misses connector root")
    h = module.R_GRAY * (module.arb.pi() / 4 - base_angle) / 2
    b = h / 2

    one_center = (
        "-6.03958742449805675289441449139725821752275343379431471883570941324e-12"
    )
    one = interval_newton(
        module,
        lambda a: return_unstable_cycles(module, base_angle, slope, a, b, 1),
        one_center,
        "1e-50",
    )

    # At the unique root, A_1 is exactly zero.  Only B_1 needs interval
    # propagation from the root enclosure.  Restarting the second cycle at
    # (0,B_1) removes the catastrophic dependency of a raw 28-collision
    # natural interval extension while preserving the exact root equation.
    _, image_stable = return_coordinates_one_cycle(
        module, base_angle, slope, one[0], b
    )
    stable_center = module.arb(image_stable.mid())
    second_center_value, _ = return_unstable_cycles(
        module, base_angle, slope, module.arb(0), stable_center, 1, differentiate="b"
    )
    _, second_derivative = return_unstable_cycles(
        module, base_angle, slope, module.arb(0), image_stable, 1, differentiate="b"
    )
    second_unstable = second_center_value + second_derivative * (
        image_stable - stable_center
    )
    _, second_stable = return_coordinates_one_cycle(
        module, base_angle, slope, module.arb(0), stable_center
    )
    if not second_unstable > 0:
        raise RuntimeError(f"second-cycle tangent defect is not positive: {second_unstable}")
    if not second_unstable > module.arb("1e-20"):
        raise RuntimeError(f"second-cycle tangent defect is too small: {second_unstable}")

    physical = shooting.certify_physical_tube(module, base_angle, slope, one[0], b)
    second_physical = shooting.certify_physical_tube(
        module, base_angle, slope, module.arb(0), image_stable
    )

    print("CONNECTOR_ONE_CYCLE_TANGENT_INVARIANCE: FALSIFIED")
    print(f"  b={b}")
    print(f"  one_cycle_root={one[0]}")
    print(f"  one_cycle_dA_da={one[2]}")
    print(f"  one_cycle_newton_image={one[3]}")
    print(f"  first_image_stable_coordinate={image_stable}")
    print(f"  second_cycle_unstable_defect={second_unstable}")
    print(f"  second_cycle_dA_db={second_derivative}")
    print(f"  second_cycle_stable_coordinate={second_stable}")
    print(f"  first_cycle_minimum_flight={physical[2]}")
    print(f"  first_cycle_minimum_target_discriminant={physical[3]}")
    print(f"  first_cycle_minimum_incidence_cosine={physical[4]}")
    print(f"  first_cycle_minimum_unintended_clearance={physical[5]}")
    print(f"  second_cycle_minimum_flight={second_physical[2]}")
    print(f"  second_cycle_minimum_target_discriminant={second_physical[3]}")
    print(f"  second_cycle_minimum_incidence_cosine={second_physical[4]}")
    print(f"  second_cycle_minimum_unintended_clearance={second_physical[5]}")
    print("  reconditioned_two_cycle_word=28 collisions / 16 returns")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=genuine graph-transform limit and full-cross inequalities")


if __name__ == "__main__":
    main()
