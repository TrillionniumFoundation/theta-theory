#!/usr/bin/env python3
"""Falsify QNL endpoint preimages in the connector test rectangle.

Use the exact full-boundary period-two QNL word

    G(0,0) -> W(0,0) -> G(0,0)

and express its fixed-section return in the connector eigenchart

    (s,p) = a (1,k) + b (1,-k).

The connector certificate proposed

    R_* = [-6.05e-12, 0] x [0,h],
    h = R_G (pi/4-theta_connector)/2.

This certificate covers all of R_* by Arb boxes, verifies the declared QNL
physical word with strict occurrence margins, and proves that its complete
unstable image lies below -0.0023.  Consequently neither target endpoint
-6.05e-12 nor 0 has a QNL preimage in R_*.  This falsifies R_* as the desired
same-rectangle connector--QNL full-cross construction; it does not falsify a
different or enlarged common rectangle.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SHOOTING_CERT = HERE / "cm2_connector_stable_shooting_tile_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def qnl_return(module, base_angle, slope, unstable, stable):
    """Return the QNL image and interval Jacobian in connector (a,b)."""

    unstable_dual = module.Dual(unstable, [module.arb(1), module.arb(0)])
    stable_dual = module.Dual(stable, [module.arb(0), module.arb(1)])
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
    gray = module.obstacle("G", 0, 0)
    white = module.obstacle("W", 0, 0)
    position = (
        gray.center[0] + gray.radius * normal[0],
        gray.center[1] + gray.radius * normal[1],
    )
    for target in (white, gray):
        position, velocity = module.ray_circle_collision(position, velocity, target)

    final_normal = (
        (position[0] - gray.center[0]) / gray.radius,
        (position[1] - gray.center[1]) / gray.radius,
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
    image_unstable = (final_arclength + final_momentum.value / slope) / 2
    image_stable = (final_arclength - final_momentum.value / slope) / 2
    unstable_row = [
        (
            module.R_GRAY * angle_derivatives[index]
            + final_momentum.derivative[index] / slope
        )
        / 2
        for index in range(2)
    ]
    stable_row = [
        (
            module.R_GRAY * angle_derivatives[index]
            - final_momentum.derivative[index] / slope
        )
        / 2
        for index in range(2)
    ]
    return (
        image_unstable,
        image_stable,
        module.arb_mat([unstable_row, stable_row]),
    )


def qnl_physical_tube(shooting, module, base_angle, slope, unstable, stable):
    """Verify that every source in a tile has the physical QNL word."""

    source_arclength = unstable + stable
    source_momentum = slope * (unstable - stable)
    source_angle = base_angle + source_arclength / module.R_GRAY
    normal = source_angle.cos(), source_angle.sin()
    tangent = -normal[1], normal[0]
    cosine_phi = (1 - source_momentum * source_momentum).sqrt()
    velocity = (
        cosine_phi * normal[0] + source_momentum * tangent[0],
        cosine_phi * normal[1] + source_momentum * tangent[1],
    )
    gray = module.obstacle("G", 0, 0)
    white = module.obstacle("W", 0, 0)
    position = (
        gray.center[0] + gray.radius * normal[0],
        gray.center[1] + gray.radius * normal[1],
    )
    minima = {"flight": None, "discriminant": None, "incidence": None,
              "clearance": None}
    source_obstacle = gray
    for occurrence, target in enumerate((white, gray), start=1):
        impact, reflected, flight, discriminant, incidence = shooting.ray_circle(
            position, velocity, target
        )
        clearance = shooting.certify_segment_clearance(
            module, position, impact, source_obstacle, target
        )
        for label, point in (("source", position), ("impact", impact)):
            if not (
                point[0] > 0 and point[0] < 1
                and point[1] > 0 and point[1] < 1
            ):
                raise RuntimeError(
                    f"wall crossing at occurrence {occurrence} {label}: {point}"
                )
        values = {
            "flight": flight,
            "discriminant": discriminant,
            "incidence": incidence,
            "clearance": clearance,
        }
        for name, value in values.items():
            minima[name] = (
                value if minima[name] is None or value < minima[name]
                else minima[name]
            )
        position, velocity, source_obstacle = impact, reflected, target
    return minima


def update_minimum(global_minima, tile_minima):
    for name, value in tile_minima.items():
        global_minima[name] = (
            value
            if global_minima[name] is None or value < global_minima[name]
            else global_minima[name]
        )


def main():
    shooting = load_module("cm2_qnl_inverse_shooting", SHOOTING_CERT)
    module = shooting.load_frozen_certificate()
    root = module.certify_orbit_root()
    connector_matrix, angle_residual, momentum_residual = module.connector_derivative(
        root.boxes[0]
    )
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("connector chart origin does not close")
    slope = module.arb(
        "6.779460879726527387379610900452463910239929566858300414751989924810597"
    )
    if not (connector_matrix[1, 0] / connector_matrix[0, 1]).sqrt().contains(slope):
        raise RuntimeError("fixed connector chart slope misses eigen-slope")
    base_angle = module.arb(module.ROOT_CENTERS[0])
    if not root.boxes[0].contains(base_angle):
        raise RuntimeError("fixed connector chart origin misses root box")

    rectangle_left = module.arb("-6.05e-12")
    rectangle_right = module.arb(0)
    h = module.R_GRAY * (module.arb.pi() / 4 - base_angle) / 2
    unstable_box = rectangle_left + (rectangle_right - rectangle_left) / 2
    unstable_box += module.arb(0, ((rectangle_right - rectangle_left) / 2).upper())
    unstable_center = (rectangle_left + rectangle_right) / 2
    unstable_radius = (unstable_box - unstable_center).abs_upper()
    subdivisions = 256
    stable_step = h / subdivisions
    target_image_ceiling = module.arb("-0.0023")
    global_minima = {
        "flight": None,
        "discriminant": None,
        "incidence": None,
        "clearance": None,
    }
    maximum_image_unstable = None
    minimum_image_stable = None
    maximum_image_stable = None
    minimum_da = None

    module.certify_lattice_exhaustion(module.arb("0.15"))
    for index in range(subdivisions):
        stable_center = (module.arb(index) + module.arb("0.5")) * stable_step
        stable_box = stable_center + module.arb(0, (stable_step / 2).upper())
        tile_minima = qnl_physical_tube(
            shooting, module, base_angle, slope, unstable_box, stable_box
        )
        update_minimum(global_minima, tile_minima)
        _wrapped_unstable, _wrapped_stable, matrix = qnl_return(
            module, base_angle, slope, unstable_box, stable_box
        )
        center_unstable, center_stable, _center_matrix = qnl_return(
            module, base_angle, slope, unstable_center, stable_center
        )
        stable_radius = (stable_box - stable_center).abs_upper()
        image_unstable = center_unstable + module.arb(
            0,
            (
                matrix[0, 0].abs_upper() * unstable_radius
                + matrix[0, 1].abs_upper() * stable_radius
            ),
        )
        image_stable = center_stable + module.arb(
            0,
            (
                matrix[1, 0].abs_upper() * unstable_radius
                + matrix[1, 1].abs_upper() * stable_radius
            ),
        )
        if not image_unstable < target_image_ceiling:
            raise RuntimeError(
                f"QNL image not separated from R_* on tile {index}: {image_unstable}"
            )
        if not image_stable > 0 or not image_stable < h:
            raise RuntimeError(
                f"QNL stable image leaves [0,h] on tile {index}: {image_stable}"
            )
        if not matrix[0, 0] > 11:
            raise RuntimeError(
                f"QNL unstable derivative loses monotonicity on tile {index}: "
                f"{matrix[0, 0]}"
            )
        maximum_image_unstable = (
            image_unstable
            if maximum_image_unstable is None or image_unstable > maximum_image_unstable
            else maximum_image_unstable
        )
        minimum_image_stable = (
            image_stable
            if minimum_image_stable is None or image_stable < minimum_image_stable
            else minimum_image_stable
        )
        maximum_image_stable = (
            image_stable
            if maximum_image_stable is None or image_stable > maximum_image_stable
            else maximum_image_stable
        )
        minimum_da = (
            matrix[0, 0]
            if minimum_da is None or matrix[0, 0] < minimum_da
            else minimum_da
        )

    thresholds = {
        "flight": module.arb("0.17"),
        "discriminant": module.arb("0.02"),
        "incidence": module.arb("0.9"),
        "clearance": module.arb("0.12"),
    }
    for name, threshold in thresholds.items():
        if global_minima[name] is None or not global_minima[name] > threshold:
            raise RuntimeError(
                f"QNL physical margin {name} fails {threshold}: {global_minima[name]}"
            )
    endpoint_gap = rectangle_left - maximum_image_unstable
    if not endpoint_gap > module.arb("0.0022"):
        raise RuntimeError(f"certified inverse-root gap is too small: {endpoint_gap}")

    print("QNL_SAME_RECTANGLE_PHYSICAL_BRANCH: CERTIFIED")
    print("  word=G(0,0)->W(0,0)->G(0,0)")
    print(f"  source_rectangle=[{rectangle_left}, {rectangle_right}] x [0, {h}]")
    print(f"  stable_subdivisions={subdivisions}")
    print(f"  minimum_flight={global_minima['flight']}")
    print(f"  minimum_target_discriminant={global_minima['discriminant']}")
    print(f"  minimum_incidence_cosine={global_minima['incidence']}")
    print(f"  minimum_unintended_obstacle_clearance={global_minima['clearance']}")
    print("  transparent_wall_crossings=0")
    print("QNL_SAME_RECTANGLE_ENDPOINT_PREIMAGES: FALSIFIED")
    print(f"  maximum_image_unstable<{maximum_image_unstable}")
    print(f"  target_unstable_interval=[{rectangle_left}, {rectangle_right}]")
    print(f"  certified_left_endpoint_gap>{endpoint_gap}")
    print(f"  minimum_dA_da>{minimum_da}")
    print(f"  image_stable_span=[{minimum_image_stable}, {maximum_image_stable}]")
    print("  inverse_roots_in_R_*=0 for targets -6.05e-12 and 0")
    print("COMMON_RECTANGLE_R_*: FALSIFIED FOR QNL FULL-CROSS")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  next=enlarge/shift rectangle or construct a different singularity-cut magnet")


if __name__ == "__main__":
    main()
