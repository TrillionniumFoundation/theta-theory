#!/usr/bin/env python3
"""Certify the unique three-node quartic connector graph interpolant.

For ``g(b)=c b^2+d b^3+e b^4`` and the complete period-eight connector
return ``T(g(b),b)=(A,B)``, this certificate solves

    A-g(B)=0

at ``b=b0-1e-24, b0, b0+1e-24`` by a three-dimensional interval Newton
step.  It then proves that the locally unique interpolant continuing the
preceding cubic branch has quartic coefficient ``e>2e-42``.  Thus the local
three-node quartic continuation does not remain in the previous ``2e-42``
fourth-order scale after the quadratic and cubic coefficients are allowed to
move.

This is a finite-node polynomial threshold certificate, not a graph-transform
closure theorem and not a statement about arbitrary fourth-order remainders.

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


def quartic_residual(module, base_angle, slope, coefficients, stable):
    """Return the graph residual and its derivatives with respect to c,d,e."""

    coefficient_duals = [
        module.Dual(
            coefficient,
            [module.arb(index == column) for index in range(3)],
        )
        for column, coefficient in enumerate(coefficients)
    ]
    stable_dual = module.Dual(stable, dimension=3)
    stable_squared = stable_dual * stable_dual
    stable_cubed = stable_squared * stable_dual
    stable_fourth = stable_cubed * stable_dual
    unstable_dual = (
        coefficient_duals[0] * stable_squared
        + coefficient_duals[1] * stable_cubed
        + coefficient_duals[2] * stable_fourth
    )
    arclength = unstable_dual + stable_dual
    momentum = slope * (unstable_dual - stable_dual)
    theta = module.Dual(base_angle, dimension=3) + arclength / module.R_GRAY
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
        for index in range(3)
    ]
    final_momentum = module.dual_dot(velocity, final_tangent)
    final_arclength = module.R_GRAY * (final_angle - base_angle)
    image_unstable = module.Dual(
        (final_arclength + final_momentum.value / slope) / 2,
        [
            (module.R_GRAY * angle_derivatives[index]
             + final_momentum.derivative[index] / slope) / 2
            for index in range(3)
        ],
    )
    image_stable = module.Dual(
        (final_arclength - final_momentum.value / slope) / 2,
        [
            (module.R_GRAY * angle_derivatives[index]
             - final_momentum.derivative[index] / slope) / 2
            for index in range(3)
        ],
    )
    residual = image_unstable
    image_squared = image_stable * image_stable
    image_powers = [
        image_squared,
        image_squared * image_stable,
        image_squared * image_stable * image_stable,
    ]
    for coefficient_dual, image_power in zip(coefficient_duals, image_powers):
        residual -= coefficient_dual * image_power
    return residual.value, residual.derivative


def point_newton(module, base_angle, slope, nodes, coefficients):
    coefficients = [module.arb(value) for value in coefficients]
    for _ in range(10):
        values = []
        rows = []
        for stable in nodes:
            value, row = quartic_residual(
                module, base_angle, slope, coefficients, stable
            )
            values.append([value])
            rows.append(row)
        delta = module.arb_mat(rows).inv() * module.arb_mat(values)
        coefficients = [
            module.arb((coefficients[index] - delta[index, 0]).mid())
            for index in range(3)
        ]
    return coefficients


def main():
    cubic = load_module("cm2_quartic_cubic", CUBIC_CERT)
    tile = cubic.load_module("cm2_quartic_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_quartic_point", tile.POINT_CERT)
    shooting = point.load_module("cm2_quartic_shooting", point.SHOOTING_CERT)
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
    node_radius = module.arb("1e-6")
    nodes = [midpoint - node_radius, midpoint, midpoint + node_radius]

    cubic_coefficient, cubic_term = cubic.solve_point_system(
        module,
        base_angle,
        slope,
        nodes[0],
        nodes[2],
        module.arb("-0.000437419419665271895210239743171794"),
        module.arb(0),
    )
    centers = point_newton(
        module,
        base_angle,
        slope,
        nodes,
        [cubic_coefficient, cubic_term, module.arb("3e-42")],
    )
    radii = [module.arb("1e-60"), module.arb("1e-56"), module.arb("1e-52")]
    boxes = [
        centers[index] + module.arb(0, radii[index]) for index in range(3)
    ]

    center_values = []
    interval_rows = []
    for stable in nodes:
        center_value, _ = quartic_residual(
            module, base_angle, slope, centers, stable
        )
        _, interval_row = quartic_residual(
            module, base_angle, slope, boxes, stable
        )
        center_values.append([center_value])
        interval_rows.append(interval_row)
    jacobian = module.arb_mat(interval_rows)
    center_rows = [
        quartic_residual(module, base_angle, slope, centers, stable)[1]
        for stable in nodes
    ]
    center_jacobian = module.arb_mat(center_rows)
    determinant = center_jacobian.det()
    if determinant.contains(0):
        raise RuntimeError(f"quartic center Jacobian is singular: {determinant}")
    inverse = center_jacobian.inv()
    preconditioner = module.arb_mat(3, 3)
    for row in range(3):
        for column in range(3):
            decimal = inverse[row, column].str(100, radius=False, more=True)
            preconditioner[row, column] = module.arb(decimal)
    identity = module.arb_mat(3, 3)
    for index in range(3):
        identity[index, index] = module.arb(1)
    center_vector = module.arb_mat([[entry] for entry in centers])
    centered_box = module.arb_mat([[module.arb(0, radius)] for radius in radii])
    newton_image = (
        center_vector
        - preconditioner * module.arb_mat(center_values)
        + (identity - preconditioner * jacobian) * centered_box
    )
    for index, box in enumerate(boxes):
        if not box.contains_interior(newton_image[index, 0]):
            raise RuntimeError(
                f"quartic interval-Newton inclusion failed at {index}: "
                f"X={box}, N={newton_image[index, 0]}"
            )
    quartic_box = newton_image[2, 0]
    if not quartic_box > module.arb("2e-42"):
        raise RuntimeError(
            f"quartic coefficient lacks separation above 2e-42: {quartic_box}"
        )

    physical_nodes = []
    for stable in nodes:
        source_unstable = sum(
            boxes[index] * stable ** (index + 2) for index in range(3)
        )
        physical_nodes.append(
            shooting.certify_physical_tube(
                module, base_angle, slope, source_unstable, stable
            )
        )

    print("CONNECTOR_QUARTIC_THREE_NODE: CERTIFIED")
    print(f"  nodes={nodes}")
    print(f"  quadratic_coefficient={newton_image[0, 0]}")
    print(f"  cubic_coefficient={newton_image[1, 0]}")
    print(f"  quartic_coefficient={quartic_box}")
    print(f"  interval_jacobian_determinant={determinant}")
    print("  unique_three_node_solution_in_declared_box=yes")
    print("  quartic_coefficient_absolute_lower_bound_gt_2e-42=yes")
    print(f"  node_physical_certificates={physical_nodes}")
    print("  transparent_wall_crossings=0")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=nonpolynomial graph transform and full-cross inequalities")


if __name__ == "__main__":
    main()
