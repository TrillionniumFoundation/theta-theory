#!/usr/bin/env python3
"""Two-stage curve-atlas certificate for the connector lower boundary.

The source curve is

    a = g(b) - 6e-20,   |b-h/2| <= 2e-11.

Instead of propagating one source interval through 28 collisions, this
certificate stops after collision 14, encloses the first-image curve by a
fresh fixed-chart rectangle, and certifies the second 14-collision word from
that rectangle.  Thus the second stage does not retain the ill-conditioned
source parameter.  The stronger monotone stable-coordinate inverse is tested
but not claimed: the current derivative enclosure wraps across zero.

The certificate proves that this translated lower branch is physical and
that its two-return stable coordinate is strictly negative everywhere on a
window twice as wide as the preceding exclusion.  It does not exclude a
more distant translation, a refitted graph, or another connector word.

The optional half-open ``--start-tile/--stop-tile`` arguments certify a
slice of the fixed 65536-tile atlas.  A full claim requires a disjoint cover
of all tile indices.  Diagnostic extrema are accumulated with Arb's rigorous
``min``/``max`` operations, not by assuming two overlapping balls are
strictly ordered.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
TRANSLATED_CERT = HERE / "cm2_connector_quartic_translated_two_return_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def chart_data(module, base_angle, slope, state):
    """Fixed-chart coordinates and derivatives for a state on the gray disk."""

    gray = module.FULL_OBSTACLES[0]
    normal = (
        (state[0] - gray.center[0]) / gray.radius,
        (state[1] - gray.center[1]) / gray.radius,
    )
    tangent = -normal[1], normal[0]
    angle = module.arb.atan2(normal[1].value, normal[0].value)
    angle_denominator = (
        normal[0].value * normal[0].value
        + normal[1].value * normal[1].value
    )
    if not angle_denominator > 0:
        raise RuntimeError(
            f"gray chart angle denominator is not separated from zero: "
            f"{angle_denominator}"
        )
    angle_derivative = [
        (
            normal[0].value * normal[1].derivative[index]
            - normal[1].value * normal[0].derivative[index]
        ) / angle_denominator
        for index in range(normal[0].dimension)
    ]
    arclength = module.Dual(
        module.R_GRAY * (angle - base_angle),
        [module.R_GRAY * entry for entry in angle_derivative],
    )
    momentum = module.dual_dot(state[2:], tangent)
    return (
        (arclength + momentum / slope) / 2,
        (arclength - momentum / slope) / 2,
    )


def compose_local_map(interior, module, centers, affine, jacobian_box,
                      remainders, radius, map_function):
    """Apply a local state map to a centered one-parameter affine enclosure."""

    state_radii = [
        affine[row][0].abs_upper() * radius + remainders[row]
        for row in range(4)
    ]
    state_boxes = [
        interior.centered_box(module, centers[row], state_radii[row])
        for row in range(4)
    ]
    interval_state = [
        module.Dual(
            state_boxes[row],
            [module.arb(int(row == column)) for column in range(4)],
        )
        for row in range(4)
    ]
    center_state = [
        module.Dual(
            centers[row],
            [module.arb(int(row == column)) for column in range(4)],
        )
        for row in range(4)
    ]
    interval_outputs = map_function(interval_state)
    center_outputs = map_function(center_state)
    local_box = interior.matrix_rows(interval_outputs)
    local_center = interior.matrix_rows(center_outputs)
    new_centers = [entry.value for entry in center_outputs]
    new_affine = [
        [sum(local_center[row][inner] * affine[inner][0] for inner in range(4))]
        for row in range(len(center_outputs))
    ]
    new_jacobian_box = [
        [sum(local_box[row][inner] * jacobian_box[inner][0] for inner in range(4))]
        for row in range(len(interval_outputs))
    ]
    affine_radii = [affine[row][0].abs_upper() * radius for row in range(4)]
    new_remainders = [
        sum(
            (local_box[row][inner] - local_center[row][inner]).abs_upper()
            * affine_radii[inner]
            + local_box[row][inner].abs_upper() * remainders[inner]
            for inner in range(4)
        )
        for row in range(len(interval_outputs))
    ]
    return new_centers, new_affine, new_jacobian_box, new_remainders, state_boxes


def certify_stage(interior, shooting, module, base_angle, slope,
                  unstable_center, stable_center, unstable_box, stable_box,
                  unstable_derivative_center, stable_derivative_center,
                  unstable_derivative_box, stable_derivative_box):
    """Certify one connector word for a one-parameter input graph."""

    # Both coordinate boxes are centered on their stated point values.  The
    # common parameter radius is read from the stable parameter box in stage
    # one and from the reparameterized stable coordinate in stage two.
    radius = (stable_box - stable_center).abs_upper()
    center_inputs = (
        module.Dual(unstable_center, [unstable_derivative_center]),
        module.Dual(stable_center, [stable_derivative_center]),
    )
    interval_inputs = (
        module.Dual(unstable_box, [unstable_derivative_box]),
        module.Dual(stable_box, [stable_derivative_box]),
    )
    center_state = interior.initial_state(module, base_angle, slope, *center_inputs)
    interval_state = interior.initial_state(module, base_angle, slope, *interval_inputs)
    centers = [entry.value for entry in center_state]
    affine = interior.matrix_rows(center_state)
    jacobian_box = interior.matrix_rows(interval_state)
    # The graph center is exact and the interval derivative encloses its
    # derivative throughout the parameter tile.  The mean-value theorem
    # therefore gives the same centered initialization used by the audited
    # one-parameter occurrence recurrence.
    remainders = [
        (jacobian_box[row][0] - affine[row][0]).abs_upper() * radius
        for row in range(4)
    ]

    minima = [None] * 4
    source_obstacle = module.FULL_OBSTACLES[0]
    module.certify_lattice_exhaustion(module.arb("0.15"))
    targets = module.FULL_OBSTACLES[1:] + module.FULL_OBSTACLES[:1]

    for occurrence, target in enumerate(targets, start=1):
        def collision(state):
            return interior.collision_data(module, state, target)[0]

        state_radii = [
            affine[row][0].abs_upper() * radius + remainders[row]
            for row in range(4)
        ]
        state_boxes = [
            interior.centered_box(module, centers[row], state_radii[row])
            for row in range(4)
        ]
        interval_identity = [
            module.Dual(
                state_boxes[row],
                [module.arb(int(row == column)) for column in range(4)],
            )
            for row in range(4)
        ]
        center_identity = [
            module.Dual(
                centers[row],
                [module.arb(int(row == column)) for column in range(4)],
            )
            for row in range(4)
        ]
        interval_outputs, interval_metrics = interior.collision_data(
            module, interval_identity, target
        )
        center_outputs, center_metrics = interior.collision_data(
            module, center_identity, target
        )
        local_box = interior.matrix_rows(interval_outputs)
        local_center = interior.matrix_rows(center_outputs)
        new_centers = [entry.value for entry in center_outputs]
        new_affine = [
            [sum(local_center[row][inner] * affine[inner][0] for inner in range(4))]
            for row in range(4)
        ]
        new_jacobian_box = [
            [sum(local_box[row][inner] * jacobian_box[inner][0] for inner in range(4))]
            for row in range(4)
        ]
        affine_radii = [affine[row][0].abs_upper() * radius for row in range(4)]
        new_remainders = [
            sum(
                (local_box[row][inner] - local_center[row][inner]).abs_upper()
                * affine_radii[inner]
                + local_box[row][inner].abs_upper() * remainders[inner]
                for inner in range(4)
            )
            for row in range(4)
        ]
        output_radii = [
            new_affine[row][0].abs_upper() * radius + new_remainders[row]
            for row in range(4)
        ]
        impact_boxes = [
            interior.centered_box(module, new_centers[row], output_radii[row])
            for row in range(2)
        ]
        metrics = [
            interior.centered_metric(
                module, center_metrics[index].value,
                interval_metrics[index].derivative, state_radii,
            )
            for index in range(3)
        ]
        flight, discriminant, incidence = metrics
        if not flight > module.arb("0.1"):
            raise RuntimeError(f"flight failed at occurrence {occurrence}: {flight}")
        if not discriminant > module.arb("0.01"):
            raise RuntimeError(
                f"discriminant failed at occurrence {occurrence}: {discriminant}"
            )
        if not incidence > module.arb("0.5"):
            raise RuntimeError(
                f"incidence failed at occurrence {occurrence}: {incidence}"
            )
        clearance = shooting.certify_segment_clearance(
            module, state_boxes[:2], impact_boxes, source_obstacle, target
        )
        if not clearance > module.arb("0.15"):
            raise RuntimeError(
                f"clearance failed at occurrence {occurrence}: {clearance}"
            )
        for label, point in (("source", state_boxes[:2]), ("impact", impact_boxes)):
            if not (point[0] > 0 and point[0] < 1 and point[1] > 0 and point[1] < 1):
                raise RuntimeError(
                    f"wall crossing at occurrence {occurrence} {label}: {point}"
                )
        values = (flight, discriminant, incidence, clearance)
        minima = [
            value if old is None else old.min(value)
            for old, value in zip(minima, values)
        ]
        centers, affine, jacobian_box, remainders = (
            new_centers, new_affine, new_jacobian_box, new_remainders
        )
        source_obstacle = target

    chart = lambda state: chart_data(module, base_angle, slope, state)
    outputs = compose_local_map(
        interior, module, centers, affine, jacobian_box,
        remainders, radius, chart,
    )
    output_centers, output_affine, output_derivatives, output_remainders, _ = outputs
    output_boxes = [
        interior.centered_box(
            module,
            output_centers[row],
            output_affine[row][0].abs_upper() * radius + output_remainders[row],
        )
        for row in range(2)
    ]
    return (
        output_centers,
        [row[0] for row in output_affine],
        [row[0] for row in output_derivatives],
        output_remainders,
        output_boxes,
        minima,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-tile", type=int, default=0)
    parser.add_argument("--stop-tile", type=int, default=None)
    arguments = parser.parse_args()

    translated = load_module("cm2_two_stage_translated", TRANSLATED_CERT)
    parent = translated.load_module("cm2_two_stage_parent", translated.PARENT_CERT)
    interior = translated.load_module(
        "cm2_two_stage_interior", translated.INTERIOR_CERT
    )
    quartic = parent.load_module("cm2_two_stage_quartic", parent.QUARTIC_CERT)
    cubic = quartic.load_module("cm2_two_stage_cubic", quartic.CUBIC_CERT)
    tile = cubic.load_module("cm2_two_stage_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_two_stage_point", tile.POINT_CERT)
    shooting = point.load_module("cm2_two_stage_shooting", point.SHOOTING_CERT)
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

    # Fixed subdivision is intentionally modest: the first word is enclosed
    # in the source parameter, while the second word sees only the contracted
    # first-image stable span.
    translation_radius = module.arb("2e-11")
    subdivisions = 65536
    start_tile = arguments.start_tile
    stop_tile = subdivisions if arguments.stop_tile is None else arguments.stop_tile
    if not (0 <= start_tile < stop_tile <= subdivisions):
        raise ValueError(
            f"invalid tile range [{start_tile},{stop_tile}) for {subdivisions} tiles"
        )
    step = 2 * translation_radius / subdivisions
    stable_left = midpoint - translation_radius
    minima = [None] * 4
    maximum_first_derivative_radius = None
    minimum_second_stable = None
    maximum_second_stable = None
    first_image_stable_lower = None
    first_image_stable_upper = None
    maximum_graph_remainder = None
    maximum_first_parameter_radius = None

    for index in range(start_tile, stop_tile):
        stable_center = stable_left + (module.arb(index) + module.arb("0.5")) * step
        source_radius = step / 2
        stable_box = stable_center + module.arb(0, source_radius.upper())
        unstable_center = translated.polynomial(coefficients, stable_center) - thickness
        unstable_box = translated.polynomial(coefficients, stable_box) - thickness
        unstable_derivative_center = translated.polynomial_derivative(
            coefficients, stable_center
        )
        unstable_derivative_box = translated.polynomial_derivative(
            coefficients, stable_box
        )
        try:
            first = certify_stage(
                interior, shooting, module, base_angle, slope,
                unstable_center, stable_center, unstable_box, stable_box,
                unstable_derivative_center, module.arb(1),
                unstable_derivative_box, module.arb(1),
            )
        except RuntimeError as error:
            raise RuntimeError(f"first-stage tile {index} failed: {error}") from error
        first_centers, first_affine, first_derivatives, first_remainders, first_boxes, first_metrics = first
        try:
            second_metrics, second_matrix = interior.certify_tile(
                parent, shooting, module, base_angle, slope,
                first_centers[0], first_centers[1], first_boxes[0], first_boxes[1],
            )
        except RuntimeError as error:
            raise RuntimeError(f"second-stage tile {index} failed: {error}") from error
        second_unstable, second_stable, _ = parent.return_map_jacobian(
            module, base_angle, slope, first_centers[0], first_centers[1]
        )
        first_radii = [
            (first_boxes[row] - first_centers[row]).abs_upper() for row in range(2)
        ]
        second_centers = (second_unstable, second_stable)
        second_boxes = []
        for row in range(2):
            error = sum(
                second_matrix[row, column].abs_upper() * first_radii[column]
                for column in range(2)
            )
            second_boxes.append(second_centers[row] + module.arb(0, error))
        if not second_boxes[1] < 0:
            raise RuntimeError(
                f"two-return stable sign failed on tile {index}: {second_boxes[1]}"
            )
        first_derivative_radius = first_derivatives[1].rad()
        maximum_first_derivative_radius = (
            first_derivative_radius
            if maximum_first_derivative_radius is None
            else maximum_first_derivative_radius.max(first_derivative_radius)
        )
        second_lower = second_boxes[1].lower()
        second_upper = second_boxes[1].upper()
        minimum_second_stable = (
            second_lower
            if minimum_second_stable is None
            else minimum_second_stable.min(second_lower)
        )
        maximum_second_stable = (
            second_upper
            if maximum_second_stable is None
            else maximum_second_stable.max(second_upper)
        )
        first_lower = first_boxes[1].lower()
        first_upper = first_boxes[1].upper()
        first_image_stable_lower = (
            first_lower
            if first_image_stable_lower is None
            else first_image_stable_lower.min(first_lower)
        )
        first_image_stable_upper = (
            first_upper
            if first_image_stable_upper is None
            else first_image_stable_upper.max(first_upper)
        )
        parameter_radius = first_radii[1]
        maximum_first_parameter_radius = (
            parameter_radius
            if maximum_first_parameter_radius is None
            else maximum_first_parameter_radius.max(parameter_radius)
        )
        minima = [
            value.lower()
            if old is None
            else old.min(value.lower())
            for old, value in zip(minima, first_metrics)
        ]
        minima = [
            value.lower()
            if old is None
            else old.min(value.lower())
            for old, value in zip(minima, second_metrics)
        ]

    full_range = start_tile == 0 and stop_tile == subdivisions
    print(
        "CONNECTOR_TWO_STAGE_RECTANGLE_ATLAS: "
        + ("CERTIFIED" if full_range else "SLICE_CERTIFIED")
    )
    print(
        "  source_stable_span="
        f"[{midpoint - translation_radius}, {midpoint + translation_radius}]"
    )
    print(f"  source_tiles={subdivisions}")
    print(f"  certified_tile_range=[{start_tile},{stop_tile})")
    print(
        "  certified_source_stable_span="
        f"[{stable_left + module.arb(start_tile) * step}, "
        f"{stable_left + module.arb(stop_tile) * step}]"
    )
    print("  monotone_stable_coordinate_inverse=NOT_CERTIFIED")
    print(f"  maximum_wrapped_dB1_db_radius={maximum_first_derivative_radius}")
    print(
        "  first_image_stable_span="
        f"[{first_image_stable_lower}, {first_image_stable_upper}]"
    )
    print(f"  maximum_stage2_parameter_radius={maximum_first_parameter_radius}")
    print(
        "CONNECTOR_TWO_STAGE_EXPANDED_TWO_RETURN_WORD: "
        + ("CERTIFIED" if full_range else "SLICE_CERTIFIED")
    )
    print("  physical_word=28 collisions / 16 fixed-section returns")
    print(f"  two_word_minima={minima}")
    print("  transparent_wall_crossings=0")
    print(
        "CONNECTOR_TWO_STAGE_EXPANDED_LOWER_STABLE_ROOT: "
        + ("FALSIFIED" if full_range else "SLICE_FALSIFIED")
    )
    print(
        "  two_return_stable_range="
        f"[{minimum_second_stable}, {maximum_second_stable}]"
    )
    if full_range:
        print("  strict_obstruction=B_2(b)<0 for every |b-h/2|<=2e-11")
    else:
        print("  strict_obstruction=B_2(b)<0 on the certified tile slice")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=more distant/refitted graph or different connector/common-QNL branch")


if __name__ == "__main__":
    main()
