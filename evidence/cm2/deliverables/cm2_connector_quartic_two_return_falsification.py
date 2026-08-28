#!/usr/bin/env python3
"""Falsify the proposed axis-aligned connector two-return full cross.

The enlarged quartic connector strip is propagated through two complete
14-collision connector words.  Centered Hessian/Jacobian mean-value bounds
certify both words and the two-return endpoint images.  The lower source
boundary crosses the unstable left side of the proposed rectangle, but its
two-return stable coordinate is strictly negative.  Hence it cannot be a
full-cross boundary in

    R_2 = [-6.05e-12, h] x [0, h].

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


def update_minimum(old, value):
    return value if old is None or value < old else old


def update_maximum(old, value):
    return value if old is None or value > old else old


def main():
    parent = load_module("cm2_two_return_parent", PARENT_CERT)
    endpoint = load_module("cm2_two_return_endpoint", ENDPOINT_CERT)
    interior = load_module("cm2_two_return_interior", INTERIOR_CERT)
    quartic = parent.load_module("cm2_two_return_quartic", parent.QUARTIC_CERT)
    cubic = quartic.load_module("cm2_two_return_cubic", quartic.CUBIC_CERT)
    tile = cubic.load_module("cm2_two_return_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_two_return_point", tile.POINT_CERT)
    shooting = point.load_module("cm2_two_return_shooting", point.SHOOTING_CERT)
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
    stable_radius = module.arb("1e-22")
    rectangle_left = module.arb("-6.05e-12")
    subdivisions = 128
    stable_left = midpoint - stable_radius
    step = 2 * stable_radius / subdivisions
    cone_width = module.arb("1e-6")
    minima = [None] * 4
    maximum_second_forward_cone_margin = None
    maximum_lower_unstable = None
    maximum_lower_stable = None
    minimum_upper_unstable = None
    minimum_upper_stable = None
    maximum_upper_stable = None

    for index in range(subdivisions):
        stable_center = stable_left + (module.arb(index) + module.arb("0.5")) * step
        stable_box = stable_center + module.arb(0, (step / 2).upper())
        polynomial_box = sum(
            coefficients[power - 2] * stable_box**power for power in range(2, 5)
        )
        polynomial_center = sum(
            coefficients[power - 2] * stable_center**power for power in range(2, 5)
        )

        for sign in (-1, 1):
            unstable_box = polynomial_box + sign * thickness
            unstable_center = polynomial_center + sign * thickness
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
            ratio = module.arb(0, cone_width)
            dominant = second_matrix[0, 0] + second_matrix[0, 1] * ratio
            transverse = second_matrix[1, 0] + second_matrix[1, 1] * ratio
            second_forward_cone_margin = cone_width * dominant - transverse.abs_upper()
            if not second_forward_cone_margin < 0:
                raise RuntimeError(
                    f"fixed-width second-word cone falsification failed on tile "
                    f"{index}: {second_forward_cone_margin}"
                )
            maximum_second_forward_cone_margin = update_maximum(
                maximum_second_forward_cone_margin, second_forward_cone_margin
            )
            second_center_unstable, second_center_stable, _ = parent.return_map_jacobian(
                module, base_angle, slope,
                first_center_unstable, first_center_stable,
            )
            first_radii = (
                (first_images[0] - first_center_unstable).abs_upper(),
                (first_images[1] - first_center_stable).abs_upper(),
            )
            second_images = []
            for row, center in enumerate((second_center_unstable, second_center_stable)):
                error = sum(
                    second_matrix[row, column].abs_upper() * first_radii[column]
                    for column in range(2)
                )
                second_images.append(center + module.arb(0, error))

            minima = [
                update_minimum(old, value)
                for old, value in zip(minima, first_physical[2:6])
            ]
            minima = [
                update_minimum(old, value)
                for old, value in zip(minima, second_metrics)
            ]

            image_unstable, image_stable = second_images
            if sign < 0:
                if not image_unstable < rectangle_left:
                    raise RuntimeError(
                        f"lower boundary misses unstable left crossing on tile {index}: "
                        f"{image_unstable}"
                    )
                if not image_stable < 0:
                    raise RuntimeError(
                        f"lower stable-coordinate falsification failed on tile {index}: "
                        f"{image_stable}"
                    )
                maximum_lower_unstable = update_maximum(
                    maximum_lower_unstable, image_unstable
                )
                maximum_lower_stable = update_maximum(maximum_lower_stable, image_stable)
            else:
                if not image_unstable > half_side:
                    raise RuntimeError(
                        f"upper boundary misses unstable right crossing on tile {index}: "
                        f"{image_unstable}"
                    )
                minimum_upper_unstable = update_minimum(
                    minimum_upper_unstable, image_unstable
                )
                minimum_upper_stable = update_minimum(minimum_upper_stable, image_stable)
                maximum_upper_stable = update_maximum(maximum_upper_stable, image_stable)

    print("CONNECTOR_QUARTIC_TWO_RETURN_WORD: CERTIFIED")
    print("  physical_word=28 collisions / 16 fixed-section returns")
    print(f"  stable_subdivisions={subdivisions}")
    print(f"  minimum_flight={minima[0]}")
    print(f"  minimum_target_discriminant={minima[1]}")
    print(f"  minimum_incidence_cosine={minima[2]}")
    print(f"  minimum_unintended_obstacle_clearance={minima[3]}")
    print("  transparent_wall_crossings=0")
    print("CONNECTOR_SECOND_WORD_FIXED_WIDTH_FORWARD_CONE: FALSIFIED")
    print(f"  cone_width={cone_width}")
    print(f"  maximum_forward_cone_margin={maximum_second_forward_cone_margin}")
    print("CONNECTOR_QUARTIC_TWO_RETURN_ENDPOINT_CROSSING: CERTIFIED")
    print(f"  rectangle=[{rectangle_left}, {half_side}] x [0, {half_side}]")
    print(f"  maximum_lower_unstable_image={maximum_lower_unstable}")
    print(f"  minimum_upper_unstable_image={minimum_upper_unstable}")
    print("CONNECTOR_QUARTIC_TWO_RETURN_FULL_CROSS: FALSIFIED")
    print(f"  maximum_lower_stable_image={maximum_lower_stable}")
    print("  strict_obstruction=lower boundary two-return stable coordinate < 0")
    print(f"  upper_stable_image_range=[{minimum_upper_stable}, {maximum_upper_stable}]")
    print("COMMON_MAGNET: NOT CERTIFIED")


if __name__ == "__main__":
    main()
