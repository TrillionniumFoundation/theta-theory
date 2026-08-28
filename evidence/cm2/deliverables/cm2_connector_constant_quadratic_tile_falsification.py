#!/usr/bin/env python3
"""Falsify a constant-quadratic connector graph on a centered tile.

Let ``F(c,b)=A(c b^2,b)-c B(c b^2,b)^2`` be the one-cycle graph
invariance residual in connector eigen-coordinates.  The preceding point
certificate isolates the unique local coefficient solving ``F(c,b0)=0``.
Here we prove that this same coefficient has strictly opposite residuals at
the two endpoints of a nondegenerate centered ``b``-tile.  We also certify
``dF/db < -9`` throughout the root enclosure and tile.

Thus no constant coefficient in the declared local curvature box can define
an invariant quadratic graph on this tile.  This does not rule out a
variable-curvature graph, for example one with a cubic term.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
POINT_CERT = HERE / "cm2_connector_quadratic_point_invariance_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def residual_with_b_derivative(module, base_angle, slope, coefficient, stable):
    """Return F, dF/db, A, and B with c held constant."""

    coefficient_dual = module.Dual(coefficient, [module.arb(0)])
    stable_dual = module.Dual(stable, [module.arb(1)])
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
    image_unstable = (final_arclength + final_momentum.value / slope) / 2
    image_unstable_derivative = (
        final_arclength_derivative + final_momentum.derivative[0] / slope
    ) / 2
    image_stable = (final_arclength - final_momentum.value / slope) / 2
    image_stable_derivative = (
        final_arclength_derivative - final_momentum.derivative[0] / slope
    ) / 2
    residual = image_unstable - coefficient * image_stable * image_stable
    residual_derivative = image_unstable_derivative - (
        2 * coefficient * image_stable * image_stable_derivative
    )
    return residual, residual_derivative, image_unstable, image_stable


def main():
    point = load_module("cm2_quadratic_point", POINT_CERT)
    shooting = point.load_module("cm2_quadratic_tile_shooting", point.SHOOTING_CERT)
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
    if not root.boxes[0].contains(base_angle):
        raise RuntimeError("fixed chart origin misses connector root")
    b0 = module.R_GRAY * (module.arb.pi() / 4 - base_angle) / 4

    local_coefficient_box = module.arb(
        "-0.000437419419665271895210239743171794", "1e-18"
    )
    _, local_derivative, _, _ = point.quadratic_residual(
        module, base_angle, slope, local_coefficient_box, b0
    )
    if not local_derivative > module.arb("1"):
        raise RuntimeError(
            f"center residual is not monotone on local box: {local_derivative}"
        )

    coefficient_domain = local_coefficient_box
    center_value = None
    coefficient_derivative = None
    for _ in range(3):
        center = module.arb(coefficient_domain.mid())
        center_value, _, _, _ = point.quadratic_residual(
            module, base_angle, slope, center, b0
        )
        _, coefficient_derivative, _, _ = point.quadratic_residual(
            module, base_angle, slope, coefficient_domain, b0
        )
        if coefficient_derivative.contains(0):
            raise RuntimeError(f"coefficient derivative contains zero: {coefficient_derivative}")
        newton_image = center - center_value / coefficient_derivative
        if not coefficient_domain.contains_interior(newton_image):
            raise RuntimeError(
                f"interval Newton inclusion failed: X={coefficient_domain}, N={newton_image}"
            )
        coefficient_domain = newton_image

    tile_radius = module.arb("1e-24")
    stable_tile = b0 + module.arb(0, "1e-24")
    left = b0 - tile_radius
    right = b0 + tile_radius
    left_residual, _, _, _ = residual_with_b_derivative(
        module, base_angle, slope, coefficient_domain, left
    )
    right_residual, _, _, _ = residual_with_b_derivative(
        module, base_angle, slope, coefficient_domain, right
    )
    _, tile_b_derivative, _, _ = residual_with_b_derivative(
        module, base_angle, slope, coefficient_domain, stable_tile
    )
    if not left_residual > module.arb("1e-24"):
        raise RuntimeError(f"left endpoint residual lacks positive margin: {left_residual}")
    if not right_residual < module.arb("-1e-24"):
        raise RuntimeError(f"right endpoint residual lacks negative margin: {right_residual}")
    if not tile_b_derivative < module.arb("-9"):
        raise RuntimeError(f"tile b-derivative lacks negative margin: {tile_b_derivative}")

    source_unstable = coefficient_domain * stable_tile * stable_tile
    physical = shooting.certify_physical_tube(
        module, base_angle, slope, source_unstable, stable_tile
    )

    print("CONNECTOR_CONSTANT_QUADRATIC_TILE: FALSIFIED")
    print(f"  center_stable_coordinate={b0}")
    print(f"  declared_tile={stable_tile}")
    print(f"  local_coefficient_box={local_coefficient_box}")
    print(f"  center_dF_dc_on_local_box={local_derivative}")
    print(f"  unique_center_coefficient={coefficient_domain}")
    print(f"  left_endpoint_residual={left_residual}")
    print(f"  right_endpoint_residual={right_residual}")
    print(f"  dF_db_on_root_box_times_tile={tile_b_derivative}")
    print("  constant_coefficient_invariant_graph_on_declared_tile=no")
    print(f"  minimum_flight={physical[2]}")
    print(f"  minimum_target_discriminant={physical[3]}")
    print(f"  minimum_incidence_cosine={physical[4]}")
    print(f"  minimum_unintended_obstacle_clearance={physical[5]}")
    print("  transparent_wall_crossings=0")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=variable-curvature graph transform and full-cross inequalities")


if __name__ == "__main__":
    main()
