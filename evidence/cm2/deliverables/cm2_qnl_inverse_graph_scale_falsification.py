#!/usr/bin/env python3
"""Certify the QNL inverse-graph scale obstruction to the current magnet.

Work in the connector eigenchart and stable span ``0 <= b <= h``.  For the
regular period-two QNL word ``G(0,0)->W(0,0)->G(0,0)``, this certificate uses
uniform scalar interval Newton to locate the inverse graphs of the current
target endpoints and of the slightly larger target envelope

    -6.46e-12 <= A_QNL <= 6.46e-12.

All four graphs lie in ``2e-4 < a < 2.139e-4``.  Independently, the two image
boundaries of the already certified enlarged connector strip stay strictly
inside the target envelope.  Hence an axis-aligned rectangle with stable span
in ``[0,h]`` that is full-crossed by this fixed connector strip must have its
right side below ``6.46e-12``; it cannot contain either QNL inverse boundary,
whose source coordinate is above ``2e-4``.

This falsifies the present one-return, axis-aligned connector--QNL construction
on the clean stable span.  It does not exclude a curved magnet, a different
connector strip, a larger stable chart, or additional iterates.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
QNL_CERT = HERE / "cm2_qnl_same_rectangle_inverse_falsification.py"
CONNECTOR_ENDPOINT_CERT = HERE / "cm2_connector_quartic_enlarged_endpoint_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def centered_a_value(qnl, module, base_angle, slope, unstable, stable_center,
                     stable_box, stable_radius):
    """Mean-value enclosure of A(unstable,b) on one stable tile."""

    center_value, _center_stable, _center_matrix = qnl.qnl_return(
        module, base_angle, slope, unstable, stable_center
    )
    _wrapped_a, _wrapped_b, derivative_box = qnl.qnl_return(
        module, base_angle, slope, unstable, stable_box
    )
    return center_value + module.arb(
        0, (derivative_box[0, 1].abs_upper() * stable_radius).upper()
    )


def point_newton(qnl, module, base_angle, slope, target, stable):
    unstable = module.arb("0.00021383")
    for _ in range(6):
        value, _image_stable, matrix = qnl.qnl_return(
            module, base_angle, slope, unstable, stable
        )
        unstable -= (value - target) / matrix[0, 0]
    return unstable


def certify_qnl_inverse_graphs(qnl, shooting, module, base_angle, slope, h,
                               target_envelope):
    root_floor = module.arb("0.0002")
    root_ceiling = module.arb("0.0002139")
    current_left = module.arb("-6.05e-12")
    targets = (
        -target_envelope,
        current_left,
        module.arb(0),
        target_envelope,
    )
    subdivisions = 1024
    stable_step = h / subdivisions
    local_radius = module.arb("2e-10")
    broad_center = (root_floor + h) / 2
    broad_box = broad_center + module.arb(
        0, ((h - root_floor) / 2).upper()
    )
    minimum_da = None
    minimum_newton_margin = None

    for index in range(subdivisions):
        stable_center = (module.arb(index) + module.arb("0.5")) * stable_step
        stable_radius = (stable_step / 2).upper()
        stable_box = stable_center + module.arb(0, stable_radius)

        # This broad derivative box makes the endpoint sign test global:
        # there is at most one root in [2e-4,h] for each fixed b and target.
        _wrapped_a, _wrapped_b, broad_matrix = qnl.qnl_return(
            module, base_angle, slope, broad_box, stable_box
        )
        if not broad_matrix[0, 0] > module.arb(5):
            raise RuntimeError(
                f"QNL broad monotonicity fails on stable tile {index}: "
                f"{broad_matrix[0, 0]}"
            )
        minimum_da = (
            broad_matrix[0, 0]
            if minimum_da is None or broad_matrix[0, 0] < minimum_da
            else minimum_da
        )
        left_value = centered_a_value(
            qnl, module, base_angle, slope, root_floor,
            stable_center, stable_box, stable_radius,
        )
        right_value = centered_a_value(
            qnl, module, base_angle, slope, h,
            stable_center, stable_box, stable_radius,
        )
        if not left_value < -target_envelope:
            raise RuntimeError(
                f"QNL lower bracket fails on stable tile {index}: {left_value}"
            )
        if not right_value > target_envelope:
            raise RuntimeError(
                f"QNL upper bracket fails on stable tile {index}: {right_value}"
            )

        # Parametric scalar interval Newton.  The endpoint signs above give
        # existence for each fixed b; strict monotonicity gives uniqueness;
        # Newton inclusion supplies the uniform, narrow source enclosure.
        for target in targets:
            center = point_newton(
                qnl, module, base_angle, slope, target, stable_center
            )
            domain = center + module.arb(0, local_radius.upper())
            center_value, _center_stable, _center_matrix = qnl.qnl_return(
                module, base_angle, slope, center, stable_center
            )
            _wrapped_center, _wrapped_stable, parameter_matrix = qnl.qnl_return(
                module, base_angle, slope, center, stable_box
            )
            _wrapped_domain, _wrapped_domain_stable, derivative_matrix = qnl.qnl_return(
                module, base_angle, slope, domain, stable_box
            )
            centered_residual = center_value - target + module.arb(
                0,
                (
                    parameter_matrix[0, 1].abs_upper() * stable_radius
                ).upper(),
            )
            derivative = derivative_matrix[0, 0]
            if derivative.contains(0):
                raise RuntimeError(
                    f"QNL Newton derivative contains zero on tile {index}: {derivative}"
                )
            newton_image = center - centered_residual / derivative
            if not domain.contains_interior(newton_image):
                raise RuntimeError(
                    f"QNL parametric Newton inclusion fails on tile {index}: "
                    f"X={domain}, N={newton_image}"
                )
            if not newton_image > root_floor or not newton_image < root_ceiling:
                raise RuntimeError(
                    f"QNL inverse graph leaves certified source range on tile "
                    f"{index}: {newton_image}"
                )
            margin = newton_image - root_floor
            minimum_newton_margin = (
                margin
                if minimum_newton_margin is None or margin < minimum_newton_margin
                else minimum_newton_margin
            )

    # Verify the physical word on one simple tube containing every Newton box.
    physical_left = module.arb("0.0002")
    physical_right = module.arb("0.0002139")
    physical_center = (physical_left + physical_right) / 2
    physical_box = physical_center + module.arb(
        0, ((physical_right - physical_left) / 2).upper()
    )
    physical_subdivisions = 256
    physical_step = h / physical_subdivisions
    minima = {
        "flight": None,
        "discriminant": None,
        "incidence": None,
        "clearance": None,
    }
    for index in range(physical_subdivisions):
        stable_center = (module.arb(index) + module.arb("0.5")) * physical_step
        stable_box = stable_center + module.arb(0, (physical_step / 2).upper())
        qnl.update_minimum(
            minima,
            qnl.qnl_physical_tube(
                shooting, module, base_angle, slope, physical_box, stable_box
            ),
        )
    thresholds = {
        "flight": module.arb("0.18"),
        "discriminant": module.arb("0.025"),
        "incidence": module.arb("0.99"),
        "clearance": module.arb("0.35"),
    }
    for name, threshold in thresholds.items():
        if minima[name] is None or not minima[name] > threshold:
            raise RuntimeError(
                f"QNL inverse-graph physical margin {name} fails: {minima[name]}"
            )
    return {
        "subdivisions": subdivisions,
        "root_floor": root_floor,
        "root_ceiling": root_ceiling,
        "minimum_da": minimum_da,
        "minimum_newton_margin": minimum_newton_margin,
        "minima": minima,
    }


def certify_connector_image_envelope(endpoint, module, base_angle, slope,
                                     target_envelope):
    parent = endpoint.load_module(
        "cm2_scale_connector_parent", endpoint.PARENT_CERT
    )
    quartic = parent.load_module(
        "cm2_scale_connector_quartic", parent.QUARTIC_CERT
    )
    cubic = quartic.load_module(
        "cm2_scale_connector_cubic", quartic.CUBIC_CERT
    )
    tile = cubic.load_module("cm2_scale_connector_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_scale_connector_point", tile.POINT_CERT)
    shooting = point.load_module(
        "cm2_scale_connector_shooting", point.SHOOTING_CERT
    )
    # Loading through the complete chain is intentional: it checks that this
    # non-frozen certificate still targets the frozen v52 geometry module.
    del shooting

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
    stable_radius = module.arb("1e-22")
    thickness = module.arb("6e-20")
    subdivisions = 128
    step = 2 * stable_radius / subdivisions
    stable_left = midpoint - stable_radius

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
        for sign in (-1, 1):
            unstable_box = polynomial_box + sign * thickness
            unstable_center = polynomial_center + sign * thickness
            images, _matrix = endpoint.mean_value_image(
                parent,
                module,
                base_angle,
                slope,
                unstable_box,
                stable_box,
                unstable_center,
                stable_center,
            )
            image_unstable = images[0]
            if not image_unstable > -target_envelope or not image_unstable < target_envelope:
                raise RuntimeError(
                    f"connector boundary leaves +/- target envelope on tile "
                    f"{index}, sign {sign}: {image_unstable}"
                )
            if sign < 0 and not image_unstable < 0:
                raise RuntimeError(
                    f"connector lower image loses orientation: {image_unstable}"
                )
            if sign > 0 and not image_unstable > 0:
                raise RuntimeError(
                    f"connector upper image loses orientation: {image_unstable}"
                )
    return subdivisions


def main():
    qnl = load_module("cm2_qnl_scale_parent", QNL_CERT)
    endpoint = load_module("cm2_connector_scale_endpoint", CONNECTOR_ENDPOINT_CERT)
    shooting = qnl.load_module("cm2_qnl_scale_shooting", qnl.SHOOTING_CERT)
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
    h = module.R_GRAY * (module.arb.pi() / 4 - base_angle) / 2
    target_envelope = module.arb("6.46e-12")

    qnl_result = certify_qnl_inverse_graphs(
        qnl, shooting, module, base_angle, slope, h, target_envelope
    )
    connector_subdivisions = certify_connector_image_envelope(
        endpoint, module, base_angle, slope, target_envelope
    )
    if not target_envelope < qnl_result["root_floor"]:
        raise RuntimeError("scale separation inequality is not strict")

    print("QNL_ENDPOINT_INVERSE_GRAPHS: CERTIFIED")
    print("  word=G(0,0)->W(0,0)->G(0,0)")
    print(f"  stable_span=[0, {h}]")
    print(f"  stable_subdivisions={qnl_result['subdivisions']}")
    print(
        "  targets={-6.46e-12,-6.05e-12,0,6.46e-12}"
    )
    print(
        f"  all_unique_source_graphs_in=({qnl_result['root_floor']}, "
        f"{qnl_result['root_ceiling']})"
    )
    print(f"  minimum_dA_da_on_[2e-4,h]={qnl_result['minimum_da']}")
    print(
        f"  minimum_source_gap_above_2e-4>"
        f"{qnl_result['minimum_newton_margin']}"
    )
    print(f"  minimum_flight={qnl_result['minima']['flight']}")
    print(
        f"  minimum_target_discriminant="
        f"{qnl_result['minima']['discriminant']}"
    )
    print(f"  minimum_incidence_cosine={qnl_result['minima']['incidence']}")
    print(
        f"  minimum_unintended_obstacle_clearance="
        f"{qnl_result['minima']['clearance']}"
    )
    print("  transparent_wall_crossings=0")
    print("CONNECTOR_BOUNDARY_IMAGE_ENVELOPE: CERTIFIED")
    print(f"  stable_subdivisions={connector_subdivisions}")
    print(f"  both_boundary_images_in=(-{target_envelope}, {target_envelope})")
    print("AXIS_ALIGNED_ONE_RETURN_COMMON_RECTANGLE_ON_[0,h]: FALSIFIED")
    print("  reason=QNL source a>2e-4 but connector-crossable right side<6.46e-12")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=curved/different/multi-return magnet and invariant stable sides")


if __name__ == "__main__":
    main()
