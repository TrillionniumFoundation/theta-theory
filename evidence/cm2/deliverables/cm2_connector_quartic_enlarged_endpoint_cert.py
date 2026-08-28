#!/usr/bin/env python3
"""Certify endpoint crossing for the enlarged connector quartic strip.

For the quartic source graph from the parent certificate, use unstable
half-thickness 6e-20 and stable interval h/2 +/- 1e-22.  The two boundary
graphs are subdivided in the stable coordinate.  On every tile this script
certifies the complete physical connector word, its singularity margins,
the centered derivative cones, and opposite unstable endpoint inequalities
for the fixed test rectangle

    R_* = [-6.05e-12, 0] x [0,h].

Only the two boundary graphs are certified by this script.  The companion
``cm2_connector_quartic_interior_tube_cert.py`` certifies the intervening
thick strip; the status of R_* as a common connector--QNL Markov rectangle is
not proved.

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


def mean_value_image(parent, module, base_angle, slope, unstable_box, stable_box,
                     unstable_center, stable_center):
    matrix, _, radii = parent.centered_jacobian_enclosure(
        module,
        base_angle,
        slope,
        unstable_box,
        stable_box,
        unstable_center,
        stable_center,
    )
    image_unstable, image_stable, _ = parent.return_map_jacobian(
        module, base_angle, slope, unstable_center, stable_center
    )
    centers = (image_unstable, image_stable)
    images = []
    for row in range(2):
        error = sum(
            matrix[row, column].abs_upper() * radii[column]
            for column in range(2)
        )
        images.append(centers[row] + module.arb(0, error))
    return images, matrix


def main():
    parent = load_module("cm2_enlarged_endpoint_parent", PARENT_CERT)
    quartic = parent.load_module(
        "cm2_enlarged_endpoint_quartic", parent.QUARTIC_CERT
    )
    cubic = quartic.load_module(
        "cm2_enlarged_endpoint_cubic", quartic.CUBIC_CERT
    )
    tile = cubic.load_module("cm2_enlarged_endpoint_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_enlarged_endpoint_point", tile.POINT_CERT)
    shooting = point.load_module(
        "cm2_enlarged_endpoint_shooting", point.SHOOTING_CERT
    )
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

    stable_radius = module.arb("1e-22")
    thickness = module.arb("6e-20")
    rectangle_left = module.arb("-6.05e-12")
    rectangle_right = module.arb(0)
    subdivisions = 128
    step = 2 * stable_radius / subdivisions
    stable_left = midpoint - stable_radius
    cone_width = module.arb("1e-6")
    expansion = module.arb(100)

    minimum_flight = None
    minimum_discriminant = None
    minimum_incidence = None
    minimum_clearance = None
    minimum_forward_cone_margin = None
    minimum_inverse_cone_margin = None
    maximum_lower_image = None
    minimum_upper_image = None
    minimum_image_stable = None
    maximum_image_stable = None

    for index in range(subdivisions):
        stable_center = stable_left + (module.arb(index) + module.arb("0.5")) * step
        stable_box = stable_center + module.arb(0, (step / 2).upper())
        polynomial_box = sum(
            coefficients[power - 2] * stable_box**power
            for power in range(2, 5)
        )
        polynomial_center = sum(
            coefficients[power - 2] * stable_center**power
            for power in range(2, 5)
        )
        source_tube = polynomial_box + module.arb(0, thickness)
        if not source_tube > rectangle_left or not source_tube < rectangle_right:
            raise RuntimeError(f"source misses R_* on tile {index}: {source_tube}")

        for sign in (-1, 1):
            unstable_box = polynomial_box + sign * thickness
            unstable_center = polynomial_center + sign * thickness
            physical = shooting.certify_physical_tube(
                module, base_angle, slope, unstable_box, stable_box
            )
            images, matrix = mean_value_image(
                parent,
                module,
                base_angle,
                slope,
                unstable_box,
                stable_box,
                unstable_center,
                stable_center,
            )
            forward_margin, _ = parent.certify_unstable_cone(
                module, matrix, cone_width, expansion
            )
            inverse_margin, _ = parent.certify_inverse_stable_cone(
                module, matrix, cone_width, expansion
            )
            image_unstable, image_stable = images
            if sign < 0:
                if not image_unstable < rectangle_left:
                    raise RuntimeError(
                        f"lower boundary fails left crossing on tile {index}: "
                        f"{image_unstable}"
                    )
                maximum_lower_image = (
                    image_unstable if maximum_lower_image is None
                    or image_unstable > maximum_lower_image else maximum_lower_image
                )
            else:
                if not image_unstable > rectangle_right:
                    raise RuntimeError(
                        f"upper boundary fails right crossing on tile {index}: "
                        f"{image_unstable}"
                    )
                minimum_upper_image = (
                    image_unstable if minimum_upper_image is None
                    or image_unstable < minimum_upper_image else minimum_upper_image
                )
            if not image_stable > 0 or not image_stable < half_side:
                raise RuntimeError(
                    f"boundary image leaves stable span on tile {index}: {image_stable}"
                )

            values = physical[2:6]
            minimum_flight = values[0] if minimum_flight is None or values[0] < minimum_flight else minimum_flight
            minimum_discriminant = values[1] if minimum_discriminant is None or values[1] < minimum_discriminant else minimum_discriminant
            minimum_incidence = values[2] if minimum_incidence is None or values[2] < minimum_incidence else minimum_incidence
            minimum_clearance = values[3] if minimum_clearance is None or values[3] < minimum_clearance else minimum_clearance
            minimum_forward_cone_margin = forward_margin if minimum_forward_cone_margin is None or forward_margin < minimum_forward_cone_margin else minimum_forward_cone_margin
            minimum_inverse_cone_margin = inverse_margin if minimum_inverse_cone_margin is None or inverse_margin < minimum_inverse_cone_margin else minimum_inverse_cone_margin
            minimum_image_stable = image_stable if minimum_image_stable is None or image_stable < minimum_image_stable else minimum_image_stable
            maximum_image_stable = image_stable if maximum_image_stable is None or image_stable > maximum_image_stable else maximum_image_stable

    print("CONNECTOR_QUARTIC_ENLARGED_BOUNDARY_ENDPOINTS: CERTIFIED")
    print(f"  half_thickness={thickness}")
    print(f"  stable_interval=[{midpoint - stable_radius}, {midpoint + stable_radius}]")
    print(f"  stable_subdivisions={subdivisions}")
    print(f"  test_rectangle=[{rectangle_left}, {rectangle_right}] x [0, {half_side}]")
    print(f"  maximum_lower_boundary_image_a<{maximum_lower_image}")
    print(f"  minimum_upper_boundary_image_a>{minimum_upper_image}")
    print(f"  image_stable_span=[{minimum_image_stable}, {maximum_image_stable}]")
    print(f"  minimum_flight={minimum_flight}")
    print(f"  minimum_target_discriminant={minimum_discriminant}")
    print(f"  minimum_incidence_cosine={minimum_incidence}")
    print(f"  minimum_unintended_obstacle_clearance={minimum_clearance}")
    print(f"  minimum_forward_cone_margin={minimum_forward_cone_margin}")
    print(f"  minimum_inverse_cone_margin={minimum_inverse_cone_margin}")
    print("  transparent_wall_crossings=0")
    print("ENLARGED_INTERIOR_PHYSICAL_TUBE: SEE COMPANION CERTIFICATE")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=invariant stable edges and common QNL rectangle")


if __name__ == "__main__":
    main()
