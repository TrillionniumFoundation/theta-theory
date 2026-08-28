#!/usr/bin/env python3
"""Exclude the two-return stable repair on ``|delta| <= 1e-11``.

The lower connector boundary is ``a=g(b)-6e-20`` with
``b=h/2+delta``.  The correlated occurrence recurrence from the local
certificate is reused on 32768 closed tiles, so the complete 28-collision
word and the strict sign ``B_2<0`` are both checked on the enlarged window.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
LOCAL_CERT = HERE / "cm2_connector_quartic_translated_two_return_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    local = load_module("cm2_expanded_translation_local", LOCAL_CERT)
    parent = local.load_module("cm2_expanded_translation_parent", local.PARENT_CERT)
    interior = local.load_module(
        "cm2_expanded_translation_interior", local.INTERIOR_CERT
    )
    quartic = parent.load_module(
        "cm2_expanded_translation_quartic", parent.QUARTIC_CERT
    )
    cubic = quartic.load_module(
        "cm2_expanded_translation_cubic", quartic.CUBIC_CERT
    )
    tile = cubic.load_module("cm2_expanded_translation_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_expanded_translation_point", tile.POINT_CERT)
    shooting = point.load_module(
        "cm2_expanded_translation_shooting", point.SHOOTING_CERT
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
    nodes = [
        midpoint - module.arb("1e-6"),
        midpoint,
        midpoint + module.arb("1e-6"),
    ]
    coefficients, _ = parent.coefficient_enclosure(
        quartic, cubic, module, base_angle, slope, nodes
    )
    thickness = module.arb("6e-20")

    translation_radius = module.arb("1e-11")
    subdivisions = 32768
    stable_left = midpoint - translation_radius
    step = 2 * translation_radius / subdivisions
    maximum_stable_upper = None
    minimum_stable_lower = None
    minimum_unstable_lower = None
    maximum_unstable_upper = None
    minima = [None] * 4
    for index in range(subdivisions):
        stable_center = stable_left + (module.arb(index) + module.arb("0.5")) * step
        stable_box = stable_center + module.arb(0, (step / 2).upper())
        try:
            images, metrics = local.certify_curve_tile(
                interior,
                shooting,
                module,
                base_angle,
                slope,
                coefficients,
                thickness,
                stable_center,
                stable_box,
            )
        except RuntimeError as error:
            raise RuntimeError(f"tile {index} failed: {error}") from error
        if not images[1].upper() < 0:
            raise RuntimeError(
                f"lower stable-image sign failed on tile {index}: {images[1]}"
            )
        stable_lower = images[1].lower()
        stable_upper = images[1].upper()
        unstable_lower = images[0].lower()
        unstable_upper = images[0].upper()
        minimum_stable_lower = (
            stable_lower
            if minimum_stable_lower is None or stable_lower < minimum_stable_lower
            else minimum_stable_lower
        )
        maximum_stable_upper = (
            stable_upper
            if maximum_stable_upper is None or stable_upper > maximum_stable_upper
            else maximum_stable_upper
        )
        minimum_unstable_lower = (
            unstable_lower
            if minimum_unstable_lower is None
            or unstable_lower < minimum_unstable_lower
            else minimum_unstable_lower
        )
        maximum_unstable_upper = (
            unstable_upper
            if maximum_unstable_upper is None
            or unstable_upper > maximum_unstable_upper
            else maximum_unstable_upper
        )
        minima = [
            value if old is None or value < old else old
            for old, value in zip(minima, metrics)
        ]

    print("CONNECTOR_EXPANDED_TRANSLATION_TWO_RETURN_WORD: CERTIFIED")
    print("  physical_word=28 collisions / 16 fixed-section returns")
    print(
        "  stable_translation_domain="
        f"[{-translation_radius}, {translation_radius}]"
    )
    print(f"  stable_subdivisions={subdivisions}")
    print(f"  two_word_minima={minima}")
    print("  transparent_wall_crossings=0")
    print("CONNECTOR_EXPANDED_TRANSLATION_LOWER_STABLE_ROOT: FALSIFIED")
    print(
        "  two_return_stable_range="
        f"[{minimum_stable_lower}, {maximum_stable_upper}]"
    )
    print(
        "  two_return_unstable_range="
        f"[{minimum_unstable_lower}, {maximum_unstable_upper}]"
    )
    print("  strict_obstruction=B_2(h/2+delta)<0 for every |delta|<=1e-11")
    print("CONNECTOR_EXPANDED_TRANSLATION_TWO_RETURN_STABLE_REPAIR: FALSIFIED")
    print("COMMON_MAGNET: NOT CERTIFIED")


if __name__ == "__main__":
    main()
