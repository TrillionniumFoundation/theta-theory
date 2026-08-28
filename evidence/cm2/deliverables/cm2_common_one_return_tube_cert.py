#!/usr/bin/env python3
"""Arb certificate for a common nonzero one-return tube.

The certified connector center and the exact QNL center both start on
G(0,0), with zero momentum, and have the same first fixed-section return word

    G(0,0) -> W(0,0) -> G(0,0).

This script encloses both centers in the rational box

    theta in 0.785 +/- 0.001,   p in 0 +/- 1e-5,

and proves, by 400-bit interval arithmetic and an exhaustive finite-lattice
clearance check, that this word is the physical first-return word throughout
the box.  It also records uniform flight, incidence, discriminant, and
unintended-obstacle clearance margins.  This is a regular-tube/singularity
margin certificate only; it does not prove that either return strip fully
crosses a common Markov rectangle.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


FROZEN_CERT = Path(__file__).with_name("cm2_fixed_section_common_vertex_cert.py")


def load_frozen_certificate():
    spec = importlib.util.spec_from_file_location("cm2_v52_common_vertex", FROZEN_CERT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load frozen certificate {FROZEN_CERT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def dot(left, right):
    return left[0] * right[0] + left[1] * right[1]


def ray_circle(position, velocity, target):
    displacement = (
        position[0] - target.center[0],
        position[1] - target.center[1],
    )
    linear = dot(displacement, velocity)
    offset = dot(displacement, displacement) - target.radius * target.radius
    discriminant = linear * linear - offset
    if not discriminant > 0:
        raise RuntimeError(f"target discriminant is not positive: {discriminant}")
    flight = -linear - discriminant.sqrt()
    if not flight > 0:
        raise RuntimeError(f"near target root is not forward: {flight}")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    normal = (
        (impact[0] - target.center[0]) / target.radius,
        (impact[1] - target.center[1]) / target.radius,
    )
    incoming_cosine = -dot(velocity, normal)
    if not incoming_cosine > 0:
        raise RuntimeError(f"target arrival is not transverse: {incoming_cosine}")
    reflected = (
        velocity[0] + 2 * incoming_cosine * normal[0],
        velocity[1] + 2 * incoming_cosine * normal[1],
    )
    return impact, reflected, flight, discriminant, incoming_cosine


def segment_distance_squared(source, target, center):
    """Interval lower bound for distance from a center to a segment."""

    direction = target[0] - source[0], target[1] - source[1]
    source_to_center = center[0] - source[0], center[1] - source[1]
    denominator = dot(direction, direction)
    projection = dot(source_to_center, direction) / denominator
    if projection < 0:
        return dot(source_to_center, source_to_center)
    if projection > 1:
        target_to_center = center[0] - target[0], center[1] - target[1]
        return dot(target_to_center, target_to_center)
    # Distance to the infinite supporting line is always a lower bound for
    # the segment distance, including when the projection interval straddles
    # an endpoint.
    return (
        dot(source_to_center, source_to_center)
        - dot(source_to_center, direction) * dot(source_to_center, direction)
        / denominator
    )


def same_obstacle(left, right):
    return (left.kind, left.i, left.j) == (right.kind, right.i, right.j)


def certify_segment_clearance(module, source, target, source_obstacle, target_obstacle):
    minimum = None
    for candidate in module.all_lattice_obstacles():
        if same_obstacle(candidate, source_obstacle) or same_obstacle(
            candidate, target_obstacle
        ):
            continue
        distance_squared = segment_distance_squared(source, target, candidate.center)
        if not distance_squared > candidate.radius * candidate.radius:
            raise RuntimeError(
                "unintended obstacle may meet segment against "
                f"{(candidate.kind, candidate.i, candidate.j)}: {distance_squared}"
            )
        clearance = distance_squared.sqrt() - candidate.radius
        minimum = clearance if minimum is None or clearance < minimum else minimum
    if minimum is None:
        raise RuntimeError("empty lattice-clearance enumeration")
    return minimum


def main() -> None:
    module = load_frozen_certificate()
    arb = module.arb

    # Exact decimal rational boxes, deliberately wider than the center hull.
    theta = arb("0.785", "0.001")
    momentum = arb(0, "1e-5")
    connector_center = arb(module.ROOT_CENTERS[0], module.ROOT_RADIUS)
    qnl_center = arb.pi() / 4
    if not theta.contains(connector_center) or not theta.contains(qnl_center):
        raise RuntimeError("rational tube does not contain both certified centers")
    if not momentum.contains(0):
        raise RuntimeError("momentum tube does not contain the center line")

    gray = module.obstacle("G", 0, 0)
    white = module.obstacle("W", 0, 0)
    minima = {"flight": None, "discriminant": None, "incidence": None, "clearance": None}

    # Subdivision controls dependency inflation through the reflection at W.
    # The 16 x 4 closed tiles cover the full rational tube, with overlap only
    # at tile boundaries.
    for theta_index in range(16):
        theta_tile = (
            arb("0.7840625")
            + theta_index * arb("0.000125")
            + arb(0, "0.0000625")
        )
        for momentum_index in range(4):
            momentum_tile = (
                arb("-0.0000075")
                + momentum_index * arb("0.000005")
                + arb(0, "0.0000025")
            )
            normal = theta_tile.cos(), theta_tile.sin()
            tangent = -normal[1], normal[0]
            # python-flint 0.9.0 returns ``nan`` for ``ball ** 2`` when the
            # ball contains zero; explicit multiplication is correct.
            cosine_phi = (1 - momentum_tile * momentum_tile).sqrt()
            velocity = (
                cosine_phi * normal[0] + momentum_tile * tangent[0],
                cosine_phi * normal[1] + momentum_tile * tangent[1],
            )
            position = (
                gray.center[0] + gray.radius * normal[0],
                gray.center[1] + gray.radius * normal[1],
            )

            white_point, after_white, flight_1, disc_1, incidence_1 = ray_circle(
                position, velocity, white
            )
            clearance_1 = certify_segment_clearance(
                module, position, white_point, gray, white
            )
            gray_point, _after_gray, flight_2, disc_2, incidence_2 = ray_circle(
                white_point, after_white, gray
            )
            clearance_2 = certify_segment_clearance(
                module, white_point, gray_point, white, gray
            )

            # Convexity then keeps both full chords inside the square.
            for label, point in (
                ("source", position),
                ("white", white_point),
                ("return", gray_point),
            ):
                if not (
                    point[0] > 0
                    and point[0] < 1
                    and point[1] > 0
                    and point[1] < 1
                ):
                    raise RuntimeError(
                        f"{label} point may leave the fundamental square: {point}"
                    )

            tile_values = {
                "flight": flight_1 if flight_1 < flight_2 else flight_2,
                "discriminant": disc_1 if disc_1 < disc_2 else disc_2,
                "incidence": incidence_1 if incidence_1 < incidence_2 else incidence_2,
                "clearance": clearance_1 if clearance_1 < clearance_2 else clearance_2,
            }
            for name, value in tile_values.items():
                if minima[name] is None or value < minima[name]:
                    minima[name] = value

    minimum_flight = minima["flight"]
    minimum_discriminant = minima["discriminant"]
    minimum_incidence = minima["incidence"]
    minimum_clearance = minima["clearance"]
    if any(value is None for value in minima.values()):
        raise RuntimeError("tube subdivision produced no margin values")

    if not minimum_flight > arb(17) / 100:
        raise RuntimeError(f"flight margin <= 0.17: {minimum_flight}")
    if not minimum_discriminant > arb(2) / 100:
        raise RuntimeError(f"discriminant margin <= 0.02: {minimum_discriminant}")
    if not minimum_incidence > arb(9) / 10:
        raise RuntimeError(f"incidence margin <= 0.9: {minimum_incidence}")
    if not minimum_clearance > arb(12) / 100:
        raise RuntimeError(f"unintended clearance margin <= 0.12: {minimum_clearance}")

    print("COMMON_ONE_RETURN_TUBE: CERTIFIED")
    print("  theta_box=0.785 +/- 0.001")
    print("  momentum_box=0 +/- 1e-5")
    print("  interval_subdivision=16x4")
    print("  physical_word=G(0,0)->W(0,0)->G(0,0)")
    print("  contains=connector_period8_center,QNL_period2_center")
    print(f"  minimum_flight={minimum_flight}")
    print(f"  minimum_target_discriminant={minimum_discriminant}")
    print(f"  minimum_incidence_cosine={minimum_incidence}")
    print(f"  minimum_unintended_obstacle_clearance={minimum_clearance}")
    print("  transparent_wall_crossings=0")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  missing=full-cross strips and strip-uniform cone graph transform")


if __name__ == "__main__":
    main()
