#!/usr/bin/env python3
"""Certify the enlarged connector quartic strip's complete interior tube.

This certificate replaces dependency-inflated natural interval iteration by
a centered affine recurrence.  At every collision, the state is represented
as a point orbit plus a two-generator affine part and a rigorous remainder.
Interval first derivatives on the current state enclosure propagate both the
remainder and a uniform Jacobian enclosure.  Every occurrence margin is then
bounded by a centered mean-value enclosure.

Together with ``cm2_connector_quartic_enlarged_endpoint_cert.py``, this proves
that the enlarged strip is a genuine local one-return full-cross candidate in
the stated test rectangle.  It does not certify invariant stable sides or a
QNL full-cross strip in the same rectangle.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT_CERT = HERE / "cm2_connector_quartic_strip_cone_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def centered_box(module, center, radius):
    return center + module.arb(0, radius.upper())


def matrix_rows(duals):
    return [list(value.derivative) for value in duals]


def total_radii(matrix, domain_radii, remainders):
    return [
        sum(row[column].abs_upper() * domain_radii[column] for column in range(2))
        + remainders[index]
        for index, row in enumerate(matrix)
    ]


def collision_data(module, state, target):
    position = state[:2]
    velocity = state[2:]
    displacement = (
        position[0] - target.center[0],
        position[1] - target.center[1],
    )
    linear = module.dual_dot(displacement, velocity)
    offset = module.dual_dot(displacement, displacement) - target.radius**2
    discriminant = linear * linear - offset
    if not discriminant.value > 0:
        raise RuntimeError(f"nonpositive centered discriminant: {discriminant.value}")
    flight = -linear - module.dual_sqrt(discriminant)
    if not flight.value > 0:
        raise RuntimeError(f"nonforward centered flight: {flight.value}")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    normal = (
        (impact[0] - target.center[0]) / target.radius,
        (impact[1] - target.center[1]) / target.radius,
    )
    arrival = -module.dual_dot(velocity, normal)
    reflected = (
        velocity[0] + 2 * arrival * normal[0],
        velocity[1] + 2 * arrival * normal[1],
    )
    return list(impact + reflected), (flight, discriminant, arrival)


def initial_state(module, base_angle, slope, unstable, stable):
    arclength = unstable + stable
    momentum = slope * (unstable - stable)
    angle = module.Dual(base_angle, dimension=unstable.dimension) + arclength / module.R_GRAY
    normal = module.dual_cos(angle), module.dual_sin(angle)
    tangent = -normal[1], normal[0]
    cosine_phi = module.dual_sqrt(1 - momentum * momentum)
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    gray = module.FULL_OBSTACLES[0]
    position = (
        gray.center[0] + gray.radius * normal[0],
        gray.center[1] + gray.radius * normal[1],
    )
    return list(position + velocity)


def centered_metric(module, center_value, interval_derivatives, state_radii):
    error = sum(
        interval_derivatives[index].abs_upper() * state_radii[index]
        for index in range(4)
    )
    return center_value + module.arb(0, error)


def certify_tile(parent, shooting, module, base_angle, slope,
                 unstable_center, stable_center, unstable_box, stable_box):
    domain_radii = (
        (unstable_box - unstable_center).abs_upper(),
        (stable_box - stable_center).abs_upper(),
    )
    center_inputs = (
        module.Dual(unstable_center, [module.arb(1), module.arb(0)]),
        module.Dual(stable_center, [module.arb(0), module.arb(1)]),
    )
    interval_inputs = (
        module.Dual(unstable_box, [module.arb(1), module.arb(0)]),
        module.Dual(stable_box, [module.arb(0), module.arb(1)]),
    )
    center_state_dual = initial_state(module, base_angle, slope, *center_inputs)
    interval_state_dual = initial_state(module, base_angle, slope, *interval_inputs)
    centers = [entry.value for entry in center_state_dual]
    affine = matrix_rows(center_state_dual)
    initial_derivatives = matrix_rows(interval_state_dual)
    jacobian_box = initial_derivatives
    remainders = [
        sum(
            (initial_derivatives[row][column] - affine[row][column]).abs_upper()
            * domain_radii[column]
            for column in range(2)
        )
        for row in range(4)
    ]

    minimum_flight = None
    minimum_discriminant = None
    minimum_incidence = None
    minimum_clearance = None
    source_obstacle = module.FULL_OBSTACLES[0]
    module.certify_lattice_exhaustion(module.arb("0.15"))

    for occurrence, target in enumerate(
        module.FULL_OBSTACLES[1:] + module.FULL_OBSTACLES[:1], start=1
    ):
        state_radii = total_radii(affine, domain_radii, remainders)
        state_boxes = [
            centered_box(module, centers[index], state_radii[index])
            for index in range(4)
        ]
        local_interval = [
            module.Dual(state_boxes[index], [module.arb(int(index == column)) for column in range(4)])
            for index in range(4)
        ]
        interval_outputs, interval_metrics = collision_data(module, local_interval, target)
        local_derivatives = matrix_rows(interval_outputs)

        local_center = [
            module.Dual(centers[index], [module.arb(int(index == column)) for column in range(4)])
            for index in range(4)
        ]
        center_outputs, center_metrics = collision_data(module, local_center, target)
        center_derivatives = matrix_rows(center_outputs)
        new_centers = [entry.value for entry in center_outputs]
        new_affine = [
            [
                sum(center_derivatives[row][inner] * affine[inner][column] for inner in range(4))
                for column in range(2)
            ]
            for row in range(4)
        ]
        new_jacobian_box = [
            [
                sum(local_derivatives[row][inner] * jacobian_box[inner][column] for inner in range(4))
                for column in range(2)
            ]
            for row in range(4)
        ]
        affine_radii = [
            sum(affine[row][column].abs_upper() * domain_radii[column] for column in range(2))
            for row in range(4)
        ]
        new_remainders = [
            sum(
                (local_derivatives[row][inner] - center_derivatives[row][inner]).abs_upper()
                * affine_radii[inner]
                + local_derivatives[row][inner].abs_upper() * remainders[inner]
                for inner in range(4)
            )
            for row in range(4)
        ]
        output_radii = total_radii(new_affine, domain_radii, new_remainders)
        impact_boxes = [
            centered_box(module, new_centers[index], output_radii[index])
            for index in range(2)
        ]
        source_boxes = state_boxes[:2]

        metrics = [
            centered_metric(module, center_metrics[index].value,
                            interval_metrics[index].derivative, state_radii)
            for index in range(3)
        ]
        flight, discriminant, incidence = metrics
        if not flight > module.arb("0.1"):
            raise RuntimeError(f"flight margin failed at occurrence {occurrence}: {flight}")
        if not discriminant > module.arb("0.01"):
            raise RuntimeError(f"discriminant margin failed at occurrence {occurrence}: {discriminant}")
        if not incidence > module.arb("0.5"):
            raise RuntimeError(f"incidence margin failed at occurrence {occurrence}: {incidence}")
        clearance = shooting.certify_segment_clearance(
            module, source_boxes, impact_boxes, source_obstacle, target
        )
        if not clearance > module.arb("0.15"):
            raise RuntimeError(f"clearance margin failed at occurrence {occurrence}: {clearance}")
        for label, point in (("source", source_boxes), ("impact", impact_boxes)):
            if not (point[0] > 0 and point[0] < 1 and point[1] > 0 and point[1] < 1):
                raise RuntimeError(f"wall crossing at occurrence {occurrence} {label}: {point}")

        minimum_flight = flight if minimum_flight is None else minimum_flight.min(flight)
        minimum_discriminant = discriminant if minimum_discriminant is None else minimum_discriminant.min(discriminant)
        minimum_incidence = incidence if minimum_incidence is None else minimum_incidence.min(incidence)
        minimum_clearance = clearance if minimum_clearance is None else minimum_clearance.min(clearance)
        centers, affine, remainders = new_centers, new_affine, new_remainders
        jacobian_box = new_jacobian_box
        source_obstacle = target

    final_radii = total_radii(affine, domain_radii, remainders)
    final_boxes = [
        centered_box(module, centers[index], final_radii[index])
        for index in range(4)
    ]
    final_normal = (
        module.Dual(final_boxes[0], jacobian_box[0]) - module.FULL_OBSTACLES[0].center[0],
        module.Dual(final_boxes[1], jacobian_box[1]) - module.FULL_OBSTACLES[0].center[1],
    )
    final_normal = (
        final_normal[0] / module.R_GRAY,
        final_normal[1] / module.R_GRAY,
    )
    final_tangent = -final_normal[1], final_normal[0]
    final_velocity = (
        module.Dual(final_boxes[2], jacobian_box[2]),
        module.Dual(final_boxes[3], jacobian_box[3]),
    )
    final_momentum = module.dual_dot(final_velocity, final_tangent)
    angle_denominator = (
        final_normal[0].value * final_normal[0].value
        + final_normal[1].value * final_normal[1].value
    )
    if not angle_denominator > 0:
        raise RuntimeError(
            f"gray chart angle denominator is not separated from zero: "
            f"{angle_denominator}"
        )
    angle_derivatives = [
        (
            final_normal[0].value * final_normal[1].derivative[index]
            - final_normal[1].value * final_normal[0].derivative[index]
        ) / angle_denominator
        for index in range(2)
    ]
    matrix = module.arb_mat([
        [(module.R_GRAY * angle_derivatives[index] + final_momentum.derivative[index] / slope) / 2 for index in range(2)],
        [(module.R_GRAY * angle_derivatives[index] - final_momentum.derivative[index] / slope) / 2 for index in range(2)],
    ])
    return (minimum_flight, minimum_discriminant, minimum_incidence, minimum_clearance), matrix


def main():
    parent = load_module("cm2_interior_parent", PARENT_CERT)
    quartic = parent.load_module("cm2_interior_quartic", parent.QUARTIC_CERT)
    cubic = quartic.load_module("cm2_interior_cubic", quartic.CUBIC_CERT)
    tile = cubic.load_module("cm2_interior_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_interior_point", tile.POINT_CERT)
    shooting = point.load_module("cm2_interior_shooting", point.SHOOTING_CERT)
    module = shooting.load_frozen_certificate()
    root = module.certify_orbit_root()
    center_matrix, angle_residual, momentum_residual = module.connector_derivative(root.boxes[0])
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("connector center does not close")
    slope = module.arb("6.779460879726527387379610900452463910239929566858300414751989924810597")
    if not (center_matrix[1, 0] / center_matrix[0, 1]).sqrt().contains(slope):
        raise RuntimeError("fixed chart slope misses certified eigen-slope")
    base_angle = module.arb(module.ROOT_CENTERS[0])
    half_side = module.R_GRAY * (module.arb.pi() / 4 - base_angle) / 2
    midpoint = half_side / 2
    nodes = [midpoint - module.arb("1e-6"), midpoint, midpoint + module.arb("1e-6")]
    coefficients, _ = parent.coefficient_enclosure(quartic, cubic, module, base_angle, slope, nodes)

    stable_radius = module.arb("1e-22")
    thickness = module.arb("6e-20")
    subdivisions = 128
    step = 2 * stable_radius / subdivisions
    stable_left = midpoint - stable_radius
    minima = [None] * 4
    minimum_forward = None
    minimum_inverse = None
    for index in range(subdivisions):
        stable_center = stable_left + (module.arb(index) + module.arb("0.5")) * step
        stable_box = stable_center + module.arb(0, (step / 2).upper())
        polynomial_box = sum(coefficients[power - 2] * stable_box**power for power in range(2, 5))
        polynomial_center = sum(coefficients[power - 2] * stable_center**power for power in range(2, 5))
        unstable_center = polynomial_center
        unstable_box = polynomial_box + module.arb(0, thickness)
        metrics, matrix = certify_tile(
            parent, shooting, module, base_angle, slope,
            unstable_center, stable_center, unstable_box, stable_box,
        )
        forward, _ = parent.certify_unstable_cone(module, matrix, module.arb("1e-6"), module.arb(100))
        inverse, _ = parent.certify_inverse_stable_cone(module, matrix, module.arb("1e-6"), module.arb(100))
        minima = [
            value if old is None else old.min(value)
            for value, old in zip(metrics, minima)
        ]
        minimum_forward = forward if minimum_forward is None else minimum_forward.min(forward)
        minimum_inverse = inverse if minimum_inverse is None else minimum_inverse.min(inverse)

    print("CONNECTOR_QUARTIC_ENLARGED_INTERIOR_TUBE: CERTIFIED")
    print(f"  half_thickness={thickness}")
    print(f"  stable_subdivisions={subdivisions}")
    print(f"  minimum_flight={minima[0]}")
    print(f"  minimum_target_discriminant={minima[1]}")
    print(f"  minimum_incidence_cosine={minima[2]}")
    print(f"  minimum_unintended_obstacle_clearance={minima[3]}")
    print(f"  minimum_forward_cone_margin={minimum_forward}")
    print(f"  minimum_inverse_cone_margin={minimum_inverse}")
    print("  transparent_wall_crossings=0")
    print("LOCAL_CONNECTOR_FULL_CROSS_CANDIDATE: CERTIFIED WITH ENDPOINT CERT")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=invariant stable sides and same-rectangle QNL full-cross strip")


if __name__ == "__main__":
    main()
