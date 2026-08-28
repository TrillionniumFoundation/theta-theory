#!/usr/bin/env python3
"""Arb certificate for a singularity separator inside any convex center hull.

The QNL period-two center and the certified period-eight connector center lie
on the zero-momentum line of the same gray collision component.  This script
proves that the open arclength segment between them contains a regular grazing
event: the outgoing normal ray from G(0,0) is tangent to G(1,0), and no other
periodic obstacle is met before that tangency.

This is a geometric constraint on a future common rectangle, not a proof or
falsification of COMMON_MAGNET.  In particular, the return map cannot be
regular on the whole convex hull; its candidate full-cross strips must be
separated by singularity cuts.

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


def main() -> None:
    module = load_frozen_certificate()
    arb = module.arb
    gray_radius = module.R_GRAY

    qnl_angle = arb(0)
    connector_angle = arb(module.ROOT_CENTERS[0])
    grazing_angle = gray_radius.asin()
    if not qnl_angle < grazing_angle < connector_angle:
        raise RuntimeError("grazing angle is not strictly between the two centers")

    sine = grazing_angle.sin()
    cosine = grazing_angle.cos()
    if not (sine - gray_radius).contains(0):
        raise RuntimeError("the proposed ray is not tangent to G(1,0)")

    source = (gray_radius * cosine, gray_radius * sine)
    flight = cosine - gray_radius
    if not flight > arb(1) / 2:
        raise RuntimeError("tangency is not a positive forward flight")
    tangent = (source[0] + flight * cosine, source[1] + flight * sine)
    target = module.obstacle("G", 1, 0)
    target_distance_squared = (
        (tangent[0] - target.center[0]) ** 2
        + (tangent[1] - target.center[1]) ** 2
    )
    if not (target_distance_squared - gray_radius**2).contains(0):
        raise RuntimeError("tangent endpoint does not lie on G(1,0)")

    minimum_clearance = None
    minimum_key = None
    for candidate in module.all_lattice_obstacles():
        key = (candidate.kind, candidate.i, candidate.j)
        if key in {("G", 0, 0), ("G", 1, 0)}:
            continue
        direction = (tangent[0] - source[0], tangent[1] - source[1])
        source_to_center = (
            candidate.center[0] - source[0],
            candidate.center[1] - source[1],
        )
        denominator = module.arb_dot(direction, direction)
        projection = module.arb_dot(source_to_center, direction) / denominator
        if projection < 0:
            distance_squared = module.arb_dot(source_to_center, source_to_center)
        elif projection > 1:
            tangent_to_center = (
                candidate.center[0] - tangent[0],
                candidate.center[1] - tangent[1],
            )
            distance_squared = module.arb_dot(tangent_to_center, tangent_to_center)
        else:
            cross = direction[0] * source_to_center[1] - direction[1] * source_to_center[0]
            distance_squared = cross**2 / denominator
        clearance = distance_squared.sqrt() - candidate.radius
        if not clearance > arb(1) / 10:
            raise RuntimeError(f"pre-tangency clearance fails for {key}: {clearance}")
        if minimum_clearance is None or clearance < minimum_clearance:
            minimum_clearance = clearance
            minimum_key = key

    if minimum_clearance is None:
        raise RuntimeError("empty obstacle enumeration")
    module.certify_lattice_exhaustion(arb(1) / 10)

    discriminant_derivative = -arb(2) * sine * cosine
    if not discriminant_derivative < -arb(2) / 3:
        raise RuntimeError("grazing discriminant is not a regular event germ")

    qnl_to_grazing = gray_radius * (grazing_angle - qnl_angle)
    grazing_to_connector = gray_radius * (connector_angle - grazing_angle)
    if not qnl_to_grazing > arb(13) / 100:
        raise RuntimeError("QNL-to-grazing arclength margin is too small")
    if not grazing_to_connector > arb(7) / 50:
        raise RuntimeError("grazing-to-connector arclength margin is too small")

    print("COMMON_RECTANGLE_SEPARATOR: CERTIFIED")
    print(f"  qnl_angle={qnl_angle}")
    print(f"  grazing_angle=asin(9/25)={grazing_angle}")
    print(f"  connector_angle={connector_angle}")
    print(f"  qnl_to_grazing_arclength={qnl_to_grazing}")
    print(f"  grazing_to_connector_arclength={grazing_to_connector}")
    print(f"  grazing_discriminant_derivative={discriminant_derivative}")
    print(f"  minimum_other_obstacle_clearance={minimum_clearance} at {minimum_key}")
    print("COMMON_REGULAR_CENTER_HULL: FALSIFIED")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  required=singularity-cut full-cross strips in one rectangle")


if __name__ == "__main__":
    main()
