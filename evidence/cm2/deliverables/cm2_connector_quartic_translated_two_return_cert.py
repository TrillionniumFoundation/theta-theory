#!/usr/bin/env python3
"""Falsify every small stable translation of the quartic two-return strip.

The lower unstable boundary is translated through ``|delta| <= 1e-12``.
A correlated one-dimensional centered occurrence recurrence certifies both
complete connector words and proves that its two-return stable coordinate
remains strictly negative throughout this window.  Thus the proposed repair
equation has no local root, even on a translation interval ten orders wider
than the certified source stable half-width.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT_CERT = HERE / "cm2_connector_quartic_strip_cone_cert.py"
ENDPOINT_CERT = HERE / "cm2_connector_quartic_enlarged_endpoint_cert.py"
INTERIOR_CERT = HERE / "cm2_connector_quartic_interior_tube_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def polynomial(coefficients, stable):
    return sum(coefficients[power - 2] * stable**power for power in range(2, 5))


def polynomial_derivative(coefficients, stable):
    return sum(
        power * coefficients[power - 2] * stable ** (power - 1)
        for power in range(2, 5)
    )


def two_return_point(parent, module, base_angle, slope, unstable, stable):
    first_unstable, first_stable, first_matrix = parent.return_map_jacobian(
        module, base_angle, slope, unstable, stable
    )
    second_unstable, second_stable, second_matrix = parent.return_map_jacobian(
        module, base_angle, slope, first_unstable, first_stable
    )
    return (second_unstable, second_stable), second_matrix * first_matrix


def enclosed_two_return(parent, endpoint, interior, shooting, module,
                        base_angle, slope, unstable_box, stable_box,
                        unstable_center, stable_center):
    first_physical = shooting.certify_physical_tube(
        module, base_angle, slope, unstable_box, stable_box
    )
    first_images, first_matrix = endpoint.mean_value_image(
        parent, module, base_angle, slope,
        unstable_box, stable_box, unstable_center, stable_center,
    )
    first_center_unstable, first_center_stable, _ = parent.return_map_jacobian(
        module, base_angle, slope, unstable_center, stable_center
    )
    second_metrics, second_matrix = interior.certify_tile(
        parent, shooting, module, base_angle, slope,
        first_center_unstable, first_center_stable,
        first_images[0], first_images[1],
    )
    second_centers, _ = two_return_point(
        parent, module, base_angle, slope, unstable_center, stable_center
    )
    first_radii = (
        (first_images[0] - first_center_unstable).abs_upper(),
        (first_images[1] - first_center_stable).abs_upper(),
    )
    second_images = []
    for row, center in enumerate(second_centers):
        error = sum(
            second_matrix[row, column].abs_upper() * first_radii[column]
            for column in range(2)
        )
        second_images.append(center + module.arb(0, error))
    return (
        second_images,
        second_matrix * first_matrix,
        tuple(first_physical[2:6]) + tuple(second_metrics),
    )


def certify_curve_tile(interior, shooting, module, base_angle, slope,
                       coefficients, thickness, stable_center, stable_box):
    """Propagate the correlated one-dimensional lower boundary for two words."""

    radius = (stable_box - stable_center).abs_upper()
    unstable_center = polynomial(coefficients, stable_center) - thickness
    unstable_box = polynomial(coefficients, stable_box) - thickness
    center_inputs = (
        module.Dual(
            unstable_center, [polynomial_derivative(coefficients, stable_center)]
        ),
        module.Dual(stable_center, [module.arb(1)]),
    )
    interval_inputs = (
        module.Dual(
            unstable_box, [polynomial_derivative(coefficients, stable_box)]
        ),
        module.Dual(stable_box, [module.arb(1)]),
    )
    center_state = interior.initial_state(module, base_angle, slope, *center_inputs)
    interval_state = interior.initial_state(module, base_angle, slope, *interval_inputs)
    centers = [entry.value for entry in center_state]
    affine = interior.matrix_rows(center_state)
    jacobian_box = interior.matrix_rows(interval_state)
    remainders = [
        (jacobian_box[row][0] - affine[row][0]).abs_upper() * radius
        for row in range(4)
    ]
    minima = [None] * 4
    source_obstacle = module.FULL_OBSTACLES[0]
    module.certify_lattice_exhaustion(module.arb("0.15"))
    targets = module.FULL_OBSTACLES[1:] + module.FULL_OBSTACLES[:1]

    for occurrence, target in enumerate(targets + targets, start=1):
        state_radii = [
            affine[row][0].abs_upper() * radius + remainders[row]
            for row in range(4)
        ]
        state_boxes = [
            interior.centered_box(module, centers[row], state_radii[row])
            for row in range(4)
        ]
        local_interval = [
            module.Dual(
                state_boxes[row],
                [module.arb(int(row == column)) for column in range(4)],
            )
            for row in range(4)
        ]
        interval_outputs, interval_metrics = interior.collision_data(
            module, local_interval, target
        )
        local_derivatives = interior.matrix_rows(interval_outputs)
        local_center = [
            module.Dual(
                centers[row],
                [module.arb(int(row == column)) for column in range(4)],
            )
            for row in range(4)
        ]
        center_outputs, center_metrics = interior.collision_data(
            module, local_center, target
        )
        center_derivatives = interior.matrix_rows(center_outputs)
        new_centers = [entry.value for entry in center_outputs]
        new_affine = [
            [sum(center_derivatives[row][inner] * affine[inner][0]
                 for inner in range(4))]
            for row in range(4)
        ]
        new_jacobian_box = [
            [sum(local_derivatives[row][inner] * jacobian_box[inner][0]
                 for inner in range(4))]
            for row in range(4)
        ]
        affine_radii = [affine[row][0].abs_upper() * radius for row in range(4)]
        new_remainders = [
            sum(
                (local_derivatives[row][inner] - center_derivatives[row][inner]).abs_upper()
                * affine_radii[inner]
                + local_derivatives[row][inner].abs_upper() * remainders[inner]
                for inner in range(4)
            )
            for row in range(4)
        ]
        output_radii = [
            new_affine[row][0].abs_upper() * radius + new_remainders[row]
            for row in range(4)
        ]
        impact_boxes = [
            interior.centered_box(module, new_centers[row], output_radii[row])
            for row in range(2)
        ]
        metrics = [
            interior.centered_metric(
                module, center_metrics[index].value,
                interval_metrics[index].derivative, state_radii,
            )
            for index in range(3)
        ]
        flight, discriminant, incidence = metrics
        if not flight > module.arb("0.1"):
            raise RuntimeError(f"flight failed at occurrence {occurrence}: {flight}")
        if not discriminant > module.arb("0.01"):
            raise RuntimeError(
                f"discriminant failed at occurrence {occurrence}: {discriminant}"
            )
        if not incidence > module.arb("0.5"):
            raise RuntimeError(
                f"incidence failed at occurrence {occurrence}: {incidence}"
            )
        clearance = shooting.certify_segment_clearance(
            module, state_boxes[:2], impact_boxes, source_obstacle, target
        )
        if not clearance > module.arb("0.15"):
            raise RuntimeError(
                f"clearance failed at occurrence {occurrence}: {clearance}"
            )
        for label, point in (("source", state_boxes[:2]), ("impact", impact_boxes)):
            if not (point[0] > 0 and point[0] < 1 and point[1] > 0 and point[1] < 1):
                raise RuntimeError(
                    f"wall crossing at occurrence {occurrence} {label}: {point}"
                )
        values = (flight, discriminant, incidence, clearance)
        minima = [
            value if old is None or value < old else old
            for old, value in zip(minima, values)
        ]
        centers, affine, jacobian_box, remainders = (
            new_centers, new_affine, new_jacobian_box, new_remainders
        )
        source_obstacle = target

    final_radii = [
        affine[row][0].abs_upper() * radius + remainders[row]
        for row in range(4)
    ]
    final_boxes = [
        interior.centered_box(module, centers[row], final_radii[row])
        for row in range(4)
    ]
    gray = module.FULL_OBSTACLES[0]
    normal = (
        (final_boxes[0] - gray.center[0]) / module.R_GRAY,
        (final_boxes[1] - gray.center[1]) / module.R_GRAY,
    )
    tangent = -normal[1], normal[0]
    momentum = final_boxes[2] * tangent[0] + final_boxes[3] * tangent[1]
    angle = module.arb.atan2(normal[1], normal[0])
    arclength = module.R_GRAY * (angle - base_angle)
    return (
        (arclength + momentum / slope) / 2,
        (arclength - momentum / slope) / 2,
    ), minima


def main():
    parent = load_module("cm2_translated_parent", PARENT_CERT)
    endpoint = load_module("cm2_translated_endpoint", ENDPOINT_CERT)
    interior = load_module("cm2_translated_interior", INTERIOR_CERT)
    quartic = parent.load_module("cm2_translated_quartic", parent.QUARTIC_CERT)
    cubic = quartic.load_module("cm2_translated_cubic", quartic.CUBIC_CERT)
    tile = cubic.load_module("cm2_translated_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_translated_point", tile.POINT_CERT)
    shooting = point.load_module("cm2_translated_shooting", point.SHOOTING_CERT)
    module = shooting.load_frozen_certificate()

    root = module.certify_orbit_root()
    center_matrix, angle_residual, momentum_residual = module.connector_derivative(
        root.boxes[0]
    )
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("connector center does not close")
    slope = module.arb(
        "6.779460879726527387379610900452463910239929566858300414751989924810597"
    )
    if not (center_matrix[1, 0] / center_matrix[0, 1]).sqrt().contains(slope):
        raise RuntimeError("fixed chart slope misses certified eigen-slope")
    base_angle = module.arb(module.ROOT_CENTERS[0])
    half_side = module.R_GRAY * (module.arb.pi() / 4 - base_angle) / 2
    midpoint = half_side / 2
    nodes = [midpoint - module.arb("1e-6"), midpoint, midpoint + module.arb("1e-6")]
    coefficients, _ = parent.coefficient_enclosure(
        quartic, cubic, module, base_angle, slope, nodes
    )
    thickness = module.arb("6e-20")

    # Kill the minimal local repair on a translation window ten orders
    # wider than the certified source half-width.  This does not claim a
    # global exclusion on [0,h].
    translation_radius = module.arb("1e-12")
    stable_left = midpoint - translation_radius
    subdivisions = 2048
    step = 2 * translation_radius / subdivisions
    maximum_stable_upper = None
    minimum_unstable_lower = None
    maximum_unstable_upper = None
    minima = [None] * 4
    for index in range(subdivisions):
        stable_center = stable_left + (module.arb(index) + module.arb("0.5")) * step
        stable_box = stable_center + module.arb(0, (step / 2).upper())
        try:
            images, metrics = certify_curve_tile(
                interior, shooting, module, base_angle, slope,
                coefficients, thickness, stable_center, stable_box,
            )
        except RuntimeError as error:
            raise RuntimeError(f"tile {index} failed: {error}") from error
        stable_upper = images[1].upper()
        unstable_lower = images[0].lower()
        unstable_upper = images[0].upper()
        if not stable_upper < 0:
            raise RuntimeError(
                f"lower stable-image sign failed on tile {index}: {images[1]}"
            )
        maximum_stable_upper = (
            stable_upper if maximum_stable_upper is None
            or stable_upper > maximum_stable_upper else maximum_stable_upper
        )
        minimum_unstable_lower = (
            unstable_lower if minimum_unstable_lower is None
            or unstable_lower < minimum_unstable_lower else minimum_unstable_lower
        )
        maximum_unstable_upper = (
            unstable_upper if maximum_unstable_upper is None
            or unstable_upper > maximum_unstable_upper else maximum_unstable_upper
        )
        minima = [
            value if old is None or value < old else old
            for old, value in zip(minima, metrics)
        ]

    print("CONNECTOR_TRANSLATED_TWO_RETURN_WORD: CERTIFIED")
    print("  physical_word=28 collisions / 16 fixed-section returns")
    print(f"  stable_translation_domain=[{-translation_radius}, {translation_radius}]")
    print(f"  stable_subdivisions={subdivisions}")
    print(f"  two_word_minima={minima}")
    print("  transparent_wall_crossings=0")
    print("CONNECTOR_TRANSLATED_LOWER_STABLE_ROOT: FALSIFIED")
    print(f"  maximum_two_return_stable_upper_bound={maximum_stable_upper}")
    print(f"  unstable_image_range=[{minimum_unstable_lower}, {maximum_unstable_upper}]")
    print("  strict_obstruction=B_2(midpoint+delta)<0 for every |delta|<=1e-12")
    print("CONNECTOR_TRANSLATED_TWO_RETURN_STABLE_CONTAINMENT: FALSIFIED")
    print("COMMON_MAGNET: NOT CERTIFIED")


if __name__ == "__main__":
    main()
