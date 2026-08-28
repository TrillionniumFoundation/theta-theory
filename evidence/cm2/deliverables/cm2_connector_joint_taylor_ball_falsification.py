#!/usr/bin/env python3
"""Falsify a joint cubic-coefficient/fourth-remainder connector graph box.

For

    g(b) = c b^2 + d b^3 + r(b),       |r(b)| <= M b^4,

this certificate allows ``c`` and ``d`` to vary in an explicit box around
the unique two-endpoint cubic interpolant.  At the left, midpoint, and right
nodes it rigorously bounds the change in the invariance residual caused by
the whole remainder ball.  A fixed linear combination of the three
polynomial residuals cancels both coefficient derivatives at the box center.
The resulting three-node defect stays separated from every remainder error,
so no graph in the declared joint box can be invariant at all three nodes.

This is a finite-node falsification, not a graph-transform closure theorem.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
FOURTH_CERT = HERE / "cm2_connector_fourth_remainder_lower_bound_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def symmetric_ball(module, radius):
    if not radius >= 0:
        raise RuntimeError(f"negative radius: {radius}")
    return module.arb(0, radius.upper())


def residual_error_bound(
    fourth,
    cubic,
    module,
    base_angle,
    slope,
    coefficient_box,
    cubic_box,
    stable,
    remainder_coefficient,
    stable_domain_right,
):
    """Bound ``|R_g-R_P|`` at one source stable coordinate.

    Here ``R_g`` is the exact graph defect for ``g=P+r`` and ``R_P`` is the
    defect returned by ``cubic_residual`` for ``P=c b^2+d b^3``.  The bound
    uses the mean-value theorem on the complete period-eight return map.
    """

    polynomial_source = coefficient_box * stable**2 + cubic_box * stable**3
    source_radius = remainder_coefficient * stable**4
    source_tube = polynomial_source + symmetric_ball(module, source_radius)
    (
        _image_unstable,
        image_stable,
        unstable_derivative,
        stable_derivative,
    ) = fourth.connector_map_derivative(
        module, base_angle, slope, source_tube, stable
    )
    stable_error = stable_derivative.abs_upper() * source_radius.upper()
    if not image_stable > 0 or not image_stable < stable_domain_right:
        raise RuntimeError(
            f"image stable coordinate leaves Taylor domain: {image_stable}"
        )
    polynomial_derivative = (
        2 * coefficient_box * image_stable
        + 3 * cubic_box * image_stable**2
    )
    error = (
        unstable_derivative.abs_upper() * source_radius.upper()
        + polynomial_derivative.abs_upper() * stable_error.upper()
        + remainder_coefficient * image_stable.abs_upper() ** 4
    )
    return module.arb(error.upper()), image_stable, source_tube


def main():
    fourth = load_module("cm2_joint_fourth", FOURTH_CERT)
    cubic = fourth.load_module("cm2_joint_cubic", fourth.CUBIC_CERT)
    tile = cubic.load_module("cm2_joint_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_joint_point", tile.POINT_CERT)
    shooting = point.load_module("cm2_joint_shooting", point.SHOOTING_CERT)
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
    midpoint = module.R_GRAY * (module.arb.pi() / 4 - base_angle) / 4
    node_radius = module.arb("1e-24")
    left, right = midpoint - node_radius, midpoint + node_radius

    coefficient_center, cubic_center = cubic.solve_point_system(
        module,
        base_angle,
        slope,
        left,
        right,
        module.arb("-0.000437419419665271895210239743171794"),
        module.arb(0),
    )
    # These radii are deliberately much wider than the endpoint displacement
    # predicted by the declared remainder size.  They are part of the joint
    # graph box tested by this certificate, not point enclosures.
    coefficient_radius = module.arb("1e-40")
    cubic_radius = module.arb("1e-36")
    coefficient_box = coefficient_center + module.arb(0, coefficient_radius)
    cubic_box = cubic_center + module.arb(0, cubic_radius)
    remainder_coefficient = module.arb("1e-55")

    center_values = []
    center_rows = []
    interval_rows = []
    for stable in (left, midpoint, right):
        value, row, _, _ = cubic.cubic_residual(
            module,
            base_angle,
            slope,
            coefficient_center,
            cubic_center,
            stable,
        )
        _, interval_row, _, _ = cubic.cubic_residual(
            module,
            base_angle,
            slope,
            coefficient_box,
            cubic_box,
            stable,
        )
        center_values.append(value)
        center_rows.append(row)
        interval_rows.append(interval_row)

    determinant = (
        center_rows[0][0] * center_rows[2][1]
        - center_rows[0][1] * center_rows[2][0]
    )
    if determinant.contains(0):
        raise RuntimeError(f"endpoint point Jacobian is singular: {determinant}")
    alpha = (
        center_rows[1][0] * center_rows[2][1]
        - center_rows[1][1] * center_rows[2][0]
    ) / determinant
    beta = (
        center_rows[0][0] * center_rows[1][1]
        - center_rows[0][1] * center_rows[1][0]
    ) / determinant
    eliminated_center_defect = (
        center_values[1] - alpha * center_values[0] - beta * center_values[2]
    )
    eliminated_gradient = [
        interval_rows[1][index]
        - alpha * interval_rows[0][index]
        - beta * interval_rows[2][index]
        for index in range(2)
    ]
    coefficient_variation = (
        eliminated_gradient[0].abs_upper() * coefficient_radius
        + eliminated_gradient[1].abs_upper() * cubic_radius
    )
    eliminated_defect_lower = (
        eliminated_center_defect.lower() - coefficient_variation.upper()
    )
    if not eliminated_defect_lower > 0:
        raise RuntimeError(
            "three-node eliminated defect loses separation on coefficient box: "
            f"{eliminated_defect_lower}"
        )

    errors = []
    image_stable_coordinates = []
    source_tubes = []
    for stable in (left, midpoint, right):
        error, image_stable, source_tube = residual_error_bound(
            fourth,
            cubic,
            module,
            base_angle,
            slope,
            coefficient_box,
            cubic_box,
            stable,
            remainder_coefficient,
            right,
        )
        errors.append(error)
        image_stable_coordinates.append(image_stable)
        source_tubes.append(source_tube)
    allowed_eliminated_error = (
        errors[1]
        + alpha.abs_upper() * errors[0]
        + beta.abs_upper() * errors[2]
    )
    # Robust endpoint Newton step with the remainder errors as interval right
    # hand sides.  This verifies that the declared coefficient box is wide
    # enough to contain the full locally induced (c,d) displacement.
    endpoint_determinant = (
        interval_rows[0][0] * interval_rows[2][1]
        - interval_rows[0][1] * interval_rows[2][0]
    )
    if endpoint_determinant.contains(0):
        raise RuntimeError(
            f"endpoint interval Jacobian is singular: {endpoint_determinant}"
        )
    left_rhs = center_values[0] + symmetric_ball(module, errors[0])
    right_rhs = center_values[2] + symmetric_ball(module, errors[2])
    coefficient_newton_image = coefficient_center - (
        interval_rows[2][1] * left_rhs
        - interval_rows[0][1] * right_rhs
    ) / endpoint_determinant
    cubic_newton_image = cubic_center - (
        -interval_rows[2][0] * left_rhs
        + interval_rows[0][0] * right_rhs
    ) / endpoint_determinant
    if not coefficient_box.contains_interior(coefficient_newton_image):
        raise RuntimeError(
            "remainder-displaced coefficient Newton image leaves box: "
            f"{coefficient_newton_image}"
        )
    if not cubic_box.contains_interior(cubic_newton_image):
        raise RuntimeError(
            "remainder-displaced cubic Newton image leaves box: "
            f"{cubic_newton_image}"
        )

    separation = eliminated_defect_lower - allowed_eliminated_error.upper()
    if not separation > module.arb("1e-50"):
        raise RuntimeError(
            "joint Taylor ball is not separated by three-node elimination: "
            f"{separation}"
        )

    stable_tile = midpoint + module.arb(0, node_radius)
    source_unstable_tile = (
        coefficient_box * stable_tile**2
        + cubic_box * stable_tile**3
        + symmetric_ball(module, remainder_coefficient * stable_tile**4)
    )
    physical = shooting.certify_physical_tube(
        module, base_angle, slope, source_unstable_tile, stable_tile
    )

    print("CONNECTOR_JOINT_TAYLOR_BALL_FALSIFICATION: CERTIFIED")
    print(f"  left_node={left}")
    print(f"  midpoint_node={midpoint}")
    print(f"  right_node={right}")
    print(f"  coefficient_box={coefficient_box}")
    print(f"  cubic_box={cubic_box}")
    print(f"  remainder_bound_M={remainder_coefficient}")
    print(f"  elimination_alpha={alpha}")
    print(f"  elimination_beta={beta}")
    print(f"  eliminated_center_defect={eliminated_center_defect}")
    print(f"  eliminated_gradient_on_box={eliminated_gradient}")
    print(f"  coefficient_variation_bound={coefficient_variation}")
    print(f"  eliminated_defect_lower_bound={eliminated_defect_lower}")
    print(f"  node_remainder_error_bounds={errors}")
    print(f"  image_stable_coordinates={image_stable_coordinates}")
    print(f"  endpoint_interval_jacobian_determinant={endpoint_determinant}")
    print(f"  remainder_displaced_coefficient_newton_image={coefficient_newton_image}")
    print(f"  remainder_displaced_cubic_newton_image={cubic_newton_image}")
    print(f"  allowed_eliminated_error={allowed_eliminated_error}")
    print(f"  final_three_node_separation={separation}")
    print("  invariant_graph_in_declared_joint_taylor_box=no")
    print(f"  minimum_flight={physical[2]}")
    print(f"  minimum_target_discriminant={physical[3]}")
    print(f"  minimum_incidence_cosine={physical[4]}")
    print(f"  minimum_unintended_obstacle_clearance={physical[5]}")
    print("  transparent_wall_crossings=0")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=larger joint graph-transform box and full-cross inequalities")


if __name__ == "__main__":
    main()
