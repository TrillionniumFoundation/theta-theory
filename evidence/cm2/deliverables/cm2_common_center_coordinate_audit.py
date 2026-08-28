#!/usr/bin/env python3
"""Arb audit of the global gray-angle coordinates of the two CM2 centers.

The QNL orbit is the normal gray--white orbit from G(0,0) to W(0,0), so its
global outward-normal angle is pi/4.  This script compares that angle with the
certified period-eight connector center and with the horizontal gray grazing
angle asin(9/25).  It falsifies the claim that the latter grazing lies between
the QNL and connector centers.

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
    white_radius = module.R_WHITE

    qnl_angle = arb.pi() / 4
    connector_angle = arb(module.ROOT_CENTERS[0])
    horizontal_grazing_angle = gray_radius.asin()

    if not horizontal_grazing_angle < connector_angle < qnl_angle:
        raise RuntimeError("certified global center ordering failed")

    sqrt_two = arb(2).sqrt()
    gray_point = (
        gray_radius * qnl_angle.cos(),
        gray_radius * qnl_angle.sin(),
    )
    white_center = (arb(1) / 2, arb(1) / 2)
    white_facing_point = (
        white_center[0] - white_radius / sqrt_two,
        white_center[1] - white_radius / sqrt_two,
    )
    displacement = (
        white_facing_point[0] - gray_point[0],
        white_facing_point[1] - gray_point[1],
    )
    cross = qnl_angle.cos() * displacement[1] - qnl_angle.sin() * displacement[0]
    if not cross.contains(0):
        raise RuntimeError("QNL gray and white facing points are not collinear")

    flight = (
        qnl_angle.cos() * displacement[0]
        + qnl_angle.sin() * displacement[1]
    )
    expected_flight = arb(1) / sqrt_two - gray_radius - white_radius
    if not (flight - expected_flight).contains(0) or not flight > arb(18) / 100:
        raise RuntimeError("QNL normal flight identity or positivity failed")

    angular_gap = qnl_angle - connector_angle
    arclength_gap = gray_radius * angular_gap
    if not angular_gap > arb(13) / 10000:
        raise RuntimeError("connector-to-QNL angular separation is too small")
    if not angular_gap < arb(14) / 10000:
        raise RuntimeError("connector-to-QNL angular separation is too large")
    if not arclength_gap > arb(46) / 100000:
        raise RuntimeError("connector-to-QNL arclength separation is too small")
    if not arclength_gap < arb(5) / 10000:
        raise RuntimeError("connector-to-QNL arclength separation is too large")

    grazing_to_connector = connector_angle - horizontal_grazing_angle
    if not grazing_to_connector > arb(2) / 5:
        raise RuntimeError("horizontal grazing is not far below both centers")

    print("COMMON_CENTER_COORDINATE_AUDIT: CERTIFIED")
    print(f"  horizontal_grazing_angle=asin(9/25)={horizontal_grazing_angle}")
    print(f"  connector_global_gray_angle={connector_angle}")
    print(f"  qnl_global_gray_angle=pi/4={qnl_angle}")
    print(f"  connector_to_qnl_angular_gap={angular_gap}")
    print(f"  connector_to_qnl_arclength_gap={arclength_gap}")
    print(f"  qnl_normal_flight={flight}")
    print("COMMON_RECTANGLE_SEPARATOR_V1: FALSIFIED")
    print("  reason=qnl_angle_was_set_to_0_instead_of_pi/4")
    print("COMMON_MAGNET: NOT CERTIFIED")


if __name__ == "__main__":
    main()
