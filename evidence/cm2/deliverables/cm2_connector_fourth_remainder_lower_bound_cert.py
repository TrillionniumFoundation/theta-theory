#!/usr/bin/env python3
"""Certify a necessary fourth-order remainder size for the connector graph.

Let ``P(b)=c b^2+d b^3``, where the coefficient box is the unique interval-
Newton solution of the two endpoint equations from
``cm2_connector_cubic_two_node_cert.py``.  Consider the Taylor ball

    g(b) = P(b) + r(b),       |r(b)| <= M |b|^4

on ``0 <= b <= b0``.  This certificate proves that ``M <= 2e-42`` is
incompatible with the graph invariance equation at ``b=b0``.  The proof
propagates the whole allowed source remainder through the complete
period-eight billiard word and subtracts the whole allowed remainder at the
image stable coordinate.  The resulting defect remains strictly positive.

This is a necessary lower bound, not an invariant graph-transform tile.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
CUBIC_CERT = HERE / "cm2_connector_cubic_two_node_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def connector_map_derivative(module, base_angle, slope, unstable, stable):
    """Return ``(A,B,dA/da,dB/da)`` on an interval source tube."""

    unstable_dual = module.Dual(unstable, [module.arb(1)])
    stable_dual = module.Dual(stable, [module.arb(0)])
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
    image_unstable = (final_arclength + final_momentum.value / slope) / 2
    image_stable = (final_arclength - final_momentum.value / slope) / 2
    unstable_derivative = (
        final_arclength_derivative + final_momentum.derivative[0] / slope
    ) / 2
    stable_derivative = (
        final_arclength_derivative - final_momentum.derivative[0] / slope
    ) / 2
    return image_unstable, image_stable, unstable_derivative, stable_derivative


def symmetric_ball(module, radius):
    """Return a zero-centered Arb ball covering ``[-radius,radius]``."""

    if not radius >= 0:
        raise RuntimeError(f"negative radius: {radius}")
    return module.arb(0, radius.upper())


def main():
    cubic = load_module("cm2_cubic_two_node", CUBIC_CERT)
    tile = cubic.load_module("cm2_fourth_remainder_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_fourth_remainder_point", tile.POINT_CERT)
    shooting = point.load_module(
        "cm2_fourth_remainder_shooting", point.SHOOTING_CERT
    )
    module = shooting.load_frozen_certificate()

    root = module.certify_orbit_root()
    matrix, angle_residual, momentum_residual = module.connector_derivative(
        root.boxes[0]
    )
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("connector center does not close")
    slope = module.arb(
        "6.779460879726527387379610900452463910239929566858300414751989924810597"
    )
    if not (matrix[1, 0] / matrix[0, 1]).sqrt().contains(slope):
        raise RuntimeError("fixed chart slope misses certified eigen-slope")
    base_angle = module.arb(module.ROOT_CENTERS[0])
    b0 = module.R_GRAY * (module.arb.pi() / 4 - base_angle) / 4
    radius = module.arb("1e-24")
    left, right = b0 - radius, b0 + radius

    coefficient_center, cubic_center = cubic.solve_point_system(
        module,
        base_angle,
        slope,
        left,
        right,
        module.arb("-0.000437419419665271895210239743171794"),
        module.arb(0),
    )
    coefficient_box = coefficient_center + module.arb(0, "1e-70")
    cubic_box = cubic_center + module.arb(0, "1e-66")

    left_center_value, _, _, _ = cubic.cubic_residual(
        module, base_angle, slope, coefficient_center, cubic_center, left
    )
    right_center_value, _, _, _ = cubic.cubic_residual(
        module, base_angle, slope, coefficient_center, cubic_center, right
    )
    _, left_row, _, _ = cubic.cubic_residual(
        module, base_angle, slope, coefficient_box, cubic_box, left
    )
    _, right_row, _, _ = cubic.cubic_residual(
        module, base_angle, slope, coefficient_box, cubic_box, right
    )
    determinant = left_row[0] * right_row[1] - left_row[1] * right_row[0]
    if determinant.contains(0):
        raise RuntimeError(f"endpoint Jacobian is singular: {determinant}")
    coefficient_root = coefficient_center - (
        right_row[1] * left_center_value - left_row[1] * right_center_value
    ) / determinant
    cubic_root = cubic_center - (
        -right_row[0] * left_center_value + left_row[0] * right_center_value
    ) / determinant
    if not coefficient_box.contains_interior(coefficient_root):
        raise RuntimeError("coefficient Newton image is not interior")
    if not cubic_box.contains_interior(cubic_root):
        raise RuntimeError("cubic Newton image is not interior")

    remainder_coefficient = module.arb("2e-42")
    source_radius = remainder_coefficient * b0**4
    source_remainder = symmetric_ball(module, source_radius)
    polynomial_source = coefficient_root * b0**2 + cubic_root * b0**3
    source_unstable = polynomial_source + source_remainder

    base_defect, _, base_image_unstable, base_image_stable = cubic.cubic_residual(
        module, base_angle, slope, coefficient_root, cubic_root, b0
    )
    _, _, unstable_derivative, stable_derivative = connector_map_derivative(
        module, base_angle, slope, source_unstable, b0
    )
    unstable_error = unstable_derivative.abs_upper() * source_radius.upper()
    stable_error = stable_derivative.abs_upper() * source_radius.upper()
    image_stable = base_image_stable + symmetric_ball(module, stable_error)
    if not image_stable > 0 or not image_stable < b0:
        raise RuntimeError(
            f"image stable coordinate leaves remainder domain: {image_stable}"
        )

    polynomial_derivative = (
        2 * coefficient_root * image_stable
        + 3 * cubic_root * image_stable**2
    )
    polynomial_error = polynomial_derivative.abs_upper() * stable_error.upper()
    output_radius = remainder_coefficient * image_stable**4
    total_error = (
        unstable_error.upper()
        + polynomial_error.upper()
        + output_radius.upper()
    )
    corrected_defect = base_defect + symmetric_ball(module, total_error)
    if not corrected_defect > module.arb("1e-50"):
        raise RuntimeError(
            "fourth-order remainder ball does not retain positive separation: "
            f"{corrected_defect}"
        )

    physical = shooting.certify_physical_tube(
        module, base_angle, slope, source_unstable, b0
    )

    print("CONNECTOR_FOURTH_REMAINDER_LOWER_BOUND: CERTIFIED")
    print(f"  stable_test_point_b0={b0}")
    print(f"  coefficient_root_box={coefficient_root}")
    print(f"  cubic_root_box={cubic_root}")
    print(f"  assumed_remainder_bound_M={remainder_coefficient}")
    print(f"  source_remainder_radius=M*b0^4={source_radius}")
    print(f"  base_polynomial_defect={base_defect}")
    print(f"  dA_da_on_source_tube={unstable_derivative}")
    print(f"  dB_da_on_source_tube={stable_derivative}")
    print(f"  propagated_unstable_error={unstable_error}")
    print(f"  propagated_stable_error={stable_error}")
    print(f"  image_stable_coordinate={image_stable}")
    print(f"  output_remainder_radius=M*B^4={output_radius}")
    print(f"  total_defect_error_bound={total_error}")
    print(f"  corrected_invariance_defect={corrected_defect}")
    print("  invariant_graph_in_declared_fourth_order_ball=no")
    print(f"  corrected_defect_lower_bound={corrected_defect.lower()}")
    print("  necessary_M_for_this_fixed_polynomial_center=>2e-42")
    print(f"  minimum_flight={physical[2]}")
    print(f"  minimum_target_discriminant={physical[3]}")
    print(f"  minimum_incidence_cosine={physical[4]}")
    print(f"  minimum_unintended_obstacle_clearance={physical[5]}")
    print("  transparent_wall_crossings=0")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=larger remainder graph transform and full-cross inequalities")


if __name__ == "__main__":
    main()
