#!/usr/bin/env python3
"""Falsify one-return full crossing for the certified quartic strip.

The parent certificate proves a physical period-eight strip with source
coordinates near ``a=-6.04e-12`` and half-thickness ``1e-25``.  This script
uses centered Jacobian enclosures and the mean-value theorem to propagate
both unstable boundary graphs.  It proves that their complete images remain
in ``|a'|<1.08e-17``.  Since the source strip lies strictly to the left of
``a=-6.03e-12``, no axis-aligned product rectangle containing that source
strip can be full-crossed by its one-return image.

This is a falsification of this strip width and this single return, not of a
larger strip, an additional iterate, or the existence of a common magnet.

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
    return images


def main(thickness_text="1e-25"):
    parent = load_module("cm2_full_cross_parent", PARENT_CERT)
    quartic = parent.load_module("cm2_full_cross_quartic", parent.QUARTIC_CERT)
    cubic = quartic.load_module("cm2_full_cross_cubic", quartic.CUBIC_CERT)
    tile = cubic.load_module("cm2_full_cross_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_full_cross_point", tile.POINT_CERT)
    shooting = point.load_module("cm2_full_cross_shooting", point.SHOOTING_CERT)
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
    coefficients, _ = parent.coefficient_enclosure(
        quartic, cubic, module, base_angle, slope, nodes
    )

    strip_radius = module.arb("1e-22")
    thickness = module.arb(thickness_text)
    subdivisions = 16
    step = 2 * strip_radius / subdivisions
    strip_left = midpoint - strip_radius
    source_right_threshold = module.arb("-6.03e-12")
    image_bound = module.arb("1.08e-17")

    for index in range(subdivisions):
        stable_center = strip_left + (module.arb(index) + module.arb("0.5")) * step
        stable_box = stable_center + module.arb(0, (step / 2).upper())
        polynomial_box = sum(
            coefficients[power - 2] * stable_box**power
            for power in range(2, 5)
        )
        polynomial_center = sum(
            coefficients[power - 2] * stable_center**power
            for power in range(2, 5)
        )
        source_box = polynomial_box + module.arb(0, thickness)
        if not source_box < source_right_threshold:
            raise RuntimeError(
                f"source separation failed on tile {index}: {source_box}"
            )
        shooting.certify_physical_tube(
            module, base_angle, slope, source_box, stable_box
        )
        for sign in (-1, 1):
            unstable_box = polynomial_box + sign * thickness
            unstable_center = polynomial_center + sign * thickness
            image_unstable, _ = mean_value_image(
                parent,
                module,
                base_angle,
                slope,
                unstable_box,
                stable_box,
                unstable_center,
                stable_center,
            )
            if not image_unstable > -image_bound or not image_unstable < image_bound:
                raise RuntimeError(
                    f"boundary image bound failed on tile {index}, sign {sign}: "
                    f"{image_unstable}"
                )

    certified_shortfall = -source_right_threshold - image_bound
    span_factor = certified_shortfall / image_bound
    if not certified_shortfall > module.arb("6.019e-12"):
        raise RuntimeError(f"insufficient certified shortfall: {certified_shortfall}")
    if not span_factor > module.arb(500_000):
        raise RuntimeError(f"insufficient span mismatch: {span_factor}")

    print("CONNECTOR_QUARTIC_ONE_RETURN_FULL_CROSS: FALSIFIED")
    print(f"  source_strip_a<{source_right_threshold}")
    print(f"  both_boundary_images_abs_a_prime<{image_bound}")
    print(f"  certified_left_endpoint_shortfall>{certified_shortfall}")
    print(f"  required_outward_span_factor>{span_factor}")
    print("  theorem=no axis-aligned product rectangle containing the source strip")
    print("          is full-crossed by this strip after one certified return")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  next=certify an enlarged physical tube or test additional returns")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} [half_thickness]")
    main(sys.argv[1] if len(sys.argv) == 2 else "1e-25")
