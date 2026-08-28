#!/usr/bin/env python3
"""Falsify a straight stable-centerline construction for the connector.

Let ``z_B`` be the certified period-eight connector center and ``z_A`` the
exact QNL center, in gray arclength--momentum coordinates.  Use the stable and
unstable eigendirections of the connector center derivative to form the
minimal product parallelogram whose opposite vertices are ``z_B`` and
``z_A``.  This script proves that the midpoint of the connector-side stable
edge follows the declared 14-collision physical word, but its period-eight
image lies strictly beyond the opposite unstable face.  Thus the straight
connector-side stable edge is not forward-contained in the product hull and
cannot be used as the centerline of a full-height stable strip whose image is
required to remain in that hull.

The conclusion is deliberately limited: curved stable sides or a larger
rectangle are not excluded, so COMMON_MAGNET is not decided.

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


def same_obstacle(left, right):
    return (left.kind, left.i, left.j) == (right.kind, right.i, right.j)


def segment_distance_squared(source, target, center):
    direction = target[0] - source[0], target[1] - source[1]
    source_to_center = center[0] - source[0], center[1] - source[1]
    denominator = dot(direction, direction)
    projection = dot(source_to_center, direction) / denominator
    if projection < 0:
        return dot(source_to_center, source_to_center)
    if projection > 1:
        target_to_center = center[0] - target[0], center[1] - target[1]
        return dot(target_to_center, target_to_center)
    # The supporting-line distance is a lower bound even if the interval
    # projection straddles an endpoint.
    projected = dot(source_to_center, direction)
    return dot(source_to_center, source_to_center) - projected * projected / denominator


def ray_circle(position, velocity, target):
    displacement = position[0] - target.center[0], position[1] - target.center[1]
    linear = dot(displacement, velocity)
    offset = dot(displacement, displacement) - target.radius * target.radius
    discriminant = linear * linear - offset
    if not discriminant > 0:
        raise RuntimeError(f"target discriminant is not positive: {discriminant}")
    flight = -linear - discriminant.sqrt()
    if not flight > 0:
        raise RuntimeError(f"near collision root is not forward: {flight}")
    impact = position[0] + flight * velocity[0], position[1] + flight * velocity[1]
    normal = (
        (impact[0] - target.center[0]) / target.radius,
        (impact[1] - target.center[1]) / target.radius,
    )
    arrival = -dot(velocity, normal)
    if not arrival > 0:
        raise RuntimeError(f"target arrival is not transverse: {arrival}")
    reflected = (
        velocity[0] + 2 * arrival * normal[0],
        velocity[1] + 2 * arrival * normal[1],
    )
    return impact, reflected, flight, discriminant, arrival


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
        raise RuntimeError("empty finite-lattice clearance enumeration")
    return minimum


def main() -> None:
    module = load_frozen_certificate()
    arb = module.arb
    root = module.certify_orbit_root()
    matrix, angle_residual, momentum_residual = module.connector_derivative(root.boxes[0])
    if not angle_residual.contains(0) or not momentum_residual.contains(0):
        raise RuntimeError("certified connector center does not close")

    # The positive/negative connector eigenlines are (1,+/- k).  Positivity
    # of the off-diagonal entries is already strict in the frozen certificate.
    slope = (matrix[1, 0] / matrix[0, 1]).sqrt()
    connector_angle = root.boxes[0]
    qnl_angle = arb.pi() / 4
    center_gap = module.R_GRAY * (qnl_angle - connector_angle)
    if not center_gap > arb("0.00046") or not center_gap < arb("0.0005"):
        raise RuntimeError(f"common-center arclength gap is unexpected: {center_gap}")

    # In coordinates (s,p)=a(1,k)+b(1,-k), the two centers are opposite
    # vertices (a,b)=(0,0) and (h,h), h=center_gap/2.  Test the midpoint
    # (a,b)=(0,h/2) of the connector-side stable edge.
    half_side = center_gap / 2
    stable_coordinate = half_side / 2
    source_arclength = stable_coordinate
    source_momentum = -slope * stable_coordinate
    source_angle = connector_angle + source_arclength / module.R_GRAY
    if not source_angle > connector_angle or not source_angle < qnl_angle:
        raise RuntimeError("stable-edge test point leaves the center-angle hull")
    if not source_momentum < arb("-0.0007") or not source_momentum > arb("-0.0009"):
        raise RuntimeError(f"stable-edge source momentum is unexpected: {source_momentum}")

    gray = module.FULL_OBSTACLES[0]
    normal = source_angle.cos(), source_angle.sin()
    tangent = -normal[1], normal[0]
    cosine_phi = (1 - source_momentum * source_momentum).sqrt()
    velocity = (
        cosine_phi * normal[0] + source_momentum * tangent[0],
        cosine_phi * normal[1] + source_momentum * tangent[1],
    )
    position = (
        gray.center[0] + gray.radius * normal[0],
        gray.center[1] + gray.radius * normal[1],
    )

    minimum_flight = None
    minimum_discriminant = None
    minimum_incidence = None
    minimum_clearance = None
    source_obstacle = gray
    targets = module.FULL_OBSTACLES[1:] + module.FULL_OBSTACLES[:1]
    module.certify_lattice_exhaustion(arb("0.15"))
    for index, target_obstacle in enumerate(targets, start=1):
        impact, reflected, flight, discriminant, incidence = ray_circle(
            position, velocity, target_obstacle
        )
        clearance = certify_segment_clearance(
            module, position, impact, source_obstacle, target_obstacle
        )
        for label, point in (("source", position), ("impact", impact)):
            if not (
                point[0] > 0
                and point[0] < 1
                and point[1] > 0
                and point[1] < 1
            ):
                raise RuntimeError(
                    f"transparent-wall crossing possible at segment {index} {label}: {point}"
                )
        minimum_flight = flight if minimum_flight is None or flight < minimum_flight else minimum_flight
        minimum_discriminant = (
            discriminant
            if minimum_discriminant is None or discriminant < minimum_discriminant
            else minimum_discriminant
        )
        minimum_incidence = incidence if minimum_incidence is None or incidence < minimum_incidence else minimum_incidence
        minimum_clearance = clearance if minimum_clearance is None or clearance < minimum_clearance else minimum_clearance
        position, velocity, source_obstacle = impact, reflected, target_obstacle

    final_normal = (
        (position[0] - gray.center[0]) / gray.radius,
        (position[1] - gray.center[1]) / gray.radius,
    )
    final_tangent = -final_normal[1], final_normal[0]
    final_angle = arb.atan2(final_normal[1], final_normal[0])
    final_momentum = dot(velocity, final_tangent)
    final_arclength = module.R_GRAY * (final_angle - connector_angle)
    final_unstable_coordinate = (final_arclength + final_momentum / slope) / 2

    if not minimum_flight > arb("0.1"):
        raise RuntimeError(f"flight margin <=0.1: {minimum_flight}")
    if not minimum_discriminant > arb("0.01"):
        raise RuntimeError(f"discriminant margin <=0.01: {minimum_discriminant}")
    if not minimum_incidence > arb("0.5"):
        raise RuntimeError(f"incidence margin <=0.5: {minimum_incidence}")
    if not minimum_clearance > arb("0.15"):
        raise RuntimeError(f"unintended clearance margin <=0.15: {minimum_clearance}")
    if not final_momentum > arb("0.004"):
        raise RuntimeError(f"final momentum does not exceed 0.004: {final_momentum}")
    if not final_unstable_coordinate > arb(2) * half_side:
        raise RuntimeError(
            "period-eight image is not separated beyond the affine hull face: "
            f"a_out={final_unstable_coordinate}, h={half_side}"
        )

    print("CONNECTOR_AFFINE_STABLE_CENTERLINE: FALSIFIED")
    print("  basis=e_plus=(1,k),e_minus=(1,-k) in gray arclength-momentum")
    print(f"  connector_eigen_slope_k={slope}")
    print(f"  center_gap={center_gap}")
    print(f"  product_hull_side_h={half_side}")
    print("  tested_source_coordinates=(a,b)=(0,h/2)")
    print(f"  source_angle={source_angle}")
    print(f"  source_momentum={source_momentum}")
    print("  physical_word=14 collisions / 8 fixed-section returns")
    print(f"  minimum_flight={minimum_flight}")
    print(f"  minimum_target_discriminant={minimum_discriminant}")
    print(f"  minimum_incidence_cosine={minimum_incidence}")
    print(f"  minimum_unintended_obstacle_clearance={minimum_clearance}")
    print("  transparent_wall_crossings=0")
    print(f"  final_momentum={final_momentum}")
    print(f"  final_unstable_coordinate={final_unstable_coordinate}")
    print("  certified_forward_containment_failure=a_out>2h>h")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=curved stable strip or enlarged common rectangle")


if __name__ == "__main__":
    main()
