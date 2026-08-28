#!/usr/bin/env python3
"""Certify a quadratic--cubic connector graph at two tile endpoints.

For ``g(b)=c b^2+d b^3`` and the period-eight connector return
``T(g(b),b)=(A,B)``, solve

    A-g(B)=0

simultaneously at ``b=b0-1e-24`` and ``b=b0+1e-24``.  A two-dimensional
interval Newton step proves existence and uniqueness in an explicit
coefficient box.  The residual of that entire unique-root enclosure is then
strictly positive at ``b=b0``.  Thus the two-node interpolant is not an
invariant graph on the interval between the nodes.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
TILE_CERT = HERE / "cm2_connector_constant_quadratic_tile_falsification.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def cubic_residual(module, base_angle, slope, coefficient, cubic, stable):
    """Return graph residual and its derivatives with respect to c,d."""

    coefficient_dual = module.Dual(
        coefficient, [module.arb(1), module.arb(0)]
    )
    cubic_dual = module.Dual(cubic, [module.arb(0), module.arb(1)])
    stable_dual = module.Dual(stable, dimension=2)
    unstable_dual = (
        coefficient_dual * stable_dual * stable_dual
        + cubic_dual * stable_dual * stable_dual * stable_dual
    )
    arclength = unstable_dual + stable_dual
    momentum = slope * (unstable_dual - stable_dual)
    theta = module.Dual(base_angle, dimension=2) + arclength / module.R_GRAY
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
    angle_derivatives = [
        final_normal[0].value * final_normal[1].derivative[index]
        - final_normal[1].value * final_normal[0].derivative[index]
        for index in range(2)
    ]
    final_momentum = module.dual_dot(velocity, final_tangent)
    final_arclength = module.R_GRAY * (final_angle - base_angle)
    image_unstable = module.Dual(
        (final_arclength + final_momentum.value / slope) / 2,
        [
            (module.R_GRAY * angle_derivatives[index]
             + final_momentum.derivative[index] / slope) / 2
            for index in range(2)
        ],
    )
    image_stable = module.Dual(
        (final_arclength - final_momentum.value / slope) / 2,
        [
            (module.R_GRAY * angle_derivatives[index]
             - final_momentum.derivative[index] / slope) / 2
            for index in range(2)
        ],
    )
    residual = (
        image_unstable
        - coefficient_dual * image_stable * image_stable
        - cubic_dual * image_stable * image_stable * image_stable
    )
    return residual.value, residual.derivative, image_unstable.value, image_stable.value


def solve_point_system(module, base_angle, slope, left, right, coefficient, cubic):
    """High-precision point Newton iteration used only as a preconditioner."""

    for _ in range(8):
        left_value, left_row, _, _ = cubic_residual(
            module, base_angle, slope, coefficient, cubic, left
        )
        right_value, right_row, _, _ = cubic_residual(
            module, base_angle, slope, coefficient, cubic, right
        )
        determinant = left_row[0] * right_row[1] - left_row[1] * right_row[0]
        if determinant.contains(0):
            raise RuntimeError(f"point Newton Jacobian is singular: {determinant}")
        delta_coefficient = (
            right_row[1] * left_value - left_row[1] * right_value
        ) / determinant
        delta_cubic = (
            -right_row[0] * left_value + left_row[0] * right_value
        ) / determinant
        coefficient = module.arb((coefficient - delta_coefficient).mid())
        cubic = module.arb((cubic - delta_cubic).mid())
    return module.arb(coefficient.mid()), module.arb(cubic.mid())


def main():
    tile = load_module("cm2_constant_quadratic_tile", TILE_CERT)
    point = tile.load_module("cm2_cubic_point", tile.POINT_CERT)
    shooting = point.load_module("cm2_cubic_shooting", point.SHOOTING_CERT)
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
    left = b0 - radius
    right = b0 + radius

    coefficient_center, cubic_center = solve_point_system(
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

    left_center_value, _, _, _ = cubic_residual(
        module, base_angle, slope, coefficient_center, cubic_center, left
    )
    right_center_value, _, _, _ = cubic_residual(
        module, base_angle, slope, coefficient_center, cubic_center, right
    )
    _, left_row, _, _ = cubic_residual(
        module, base_angle, slope, coefficient_box, cubic_box, left
    )
    _, right_row, _, _ = cubic_residual(
        module, base_angle, slope, coefficient_box, cubic_box, right
    )
    determinant = left_row[0] * right_row[1] - left_row[1] * right_row[0]
    if determinant.contains(0):
        raise RuntimeError(f"interval Jacobian is singular: {determinant}")
    newton_coefficient = coefficient_center - (
        right_row[1] * left_center_value - left_row[1] * right_center_value
    ) / determinant
    newton_cubic = cubic_center - (
        -right_row[0] * left_center_value + left_row[0] * right_center_value
    ) / determinant
    if not coefficient_box.contains_interior(newton_coefficient):
        raise RuntimeError(
            f"coefficient interval-Newton inclusion failed: {newton_coefficient}"
        )
    if not cubic_box.contains_interior(newton_cubic):
        raise RuntimeError(f"cubic interval-Newton inclusion failed: {newton_cubic}")

    midpoint_residual, _, _, _ = cubic_residual(
        module, base_angle, slope, newton_coefficient, newton_cubic, b0
    )
    if not midpoint_residual > module.arb("1e-50"):
        raise RuntimeError(
            f"midpoint residual lacks strict positive separation: {midpoint_residual}"
        )

    stable_tile = b0 + module.arb(0, "1e-24")
    source_unstable = (
        coefficient_box * stable_tile * stable_tile
        + cubic_box * stable_tile * stable_tile * stable_tile
    )
    physical = shooting.certify_physical_tube(
        module, base_angle, slope, source_unstable, stable_tile
    )

    print("CONNECTOR_CUBIC_TWO_NODE: CERTIFIED")
    print(f"  left_node={left}")
    print(f"  right_node={right}")
    print(f"  coefficient_box={coefficient_box}")
    print(f"  cubic_box={cubic_box}")
    print(f"  interval_jacobian_determinant={determinant}")
    print(f"  coefficient_newton_image={newton_coefficient}")
    print(f"  cubic_newton_image={newton_cubic}")
    print("  unique_two_node_solution=yes")
    print(f"  midpoint_residual_of_unique_root={midpoint_residual}")
    print("  invariant_quadratic_cubic_graph_on_declared_tile=no")
    print(f"  minimum_flight={physical[2]}")
    print(f"  minimum_target_discriminant={physical[3]}")
    print(f"  minimum_incidence_cosine={physical[4]}")
    print(f"  minimum_unintended_obstacle_clearance={physical[5]}")
    print("  transparent_wall_crossings=0")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=nonpolynomial graph transform and full-cross inequalities")


if __name__ == "__main__":
    main()
