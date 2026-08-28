#!/usr/bin/env python3
"""Certify a physical two-dimensional connector strip.

The strip is a small thickening of the unique three-node quartic interpolant

    a = c b^2 + d b^3 + e b^4

from ``cm2_connector_quartic_three_node_cert.py``.  On a nondegenerate stable
interval about its middle node, every subdivision tile is checked for the
complete 14-collision/eight-return word with strict singularity margins.

This is a local physical strip certificate.  A centered second-order jet
also encloses the derivative on every subdivision tile and proves uniform
forward-unstable and inverse-stable cone margins.  It does not prove that a
strip boundary is an invariant stable manifold and it does not prove full
crossing of a common Markov rectangle.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
QUARTIC_CERT = HERE / "cm2_connector_quartic_three_node_cert.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Jet2:
    """Second-order two-variable jet with Arb interval coefficients."""

    __slots__ = ("value", "gradient", "hessian")

    def __init__(self, value, gradient=None, hessian=None):
        self.value = value
        zero = type(value)(0)
        self.gradient = list(gradient) if gradient is not None else [zero, zero]
        self.hessian = (
            [list(row) for row in hessian]
            if hessian is not None
            else [[zero, zero], [zero, zero]]
        )

    def coerce(self, other):
        return other if isinstance(other, Jet2) else Jet2(type(self.value)(other))

    def __add__(self, other):
        other = self.coerce(other)
        return Jet2(
            self.value + other.value,
            [self.gradient[i] + other.gradient[i] for i in range(2)],
            [
                [self.hessian[i][j] + other.hessian[i][j] for j in range(2)]
                for i in range(2)
            ],
        )

    __radd__ = __add__

    def __neg__(self):
        return Jet2(
            -self.value,
            [-entry for entry in self.gradient],
            [[-entry for entry in row] for row in self.hessian],
        )

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return Jet2(
            self.value * other.value,
            [
                self.gradient[i] * other.value
                + self.value * other.gradient[i]
                for i in range(2)
            ],
            [
                [
                    self.hessian[i][j] * other.value
                    + self.gradient[i] * other.gradient[j]
                    + self.gradient[j] * other.gradient[i]
                    + self.value * other.hessian[i][j]
                    for j in range(2)
                ]
                for i in range(2)
            ],
        )

    __rmul__ = __mul__

    def unary(self, value, first, second):
        return Jet2(
            value,
            [first * entry for entry in self.gradient],
            [
                [
                    second * self.gradient[i] * self.gradient[j]
                    + first * self.hessian[i][j]
                    for j in range(2)
                ]
                for i in range(2)
            ],
        )

    def reciprocal(self):
        return self.unary(
            1 / self.value,
            -1 / self.value**2,
            2 / self.value**3,
        )

    def __truediv__(self, other):
        return self * self.coerce(other).reciprocal()

    def __rtruediv__(self, other):
        return self.coerce(other) / self


def jet_sin(value):
    return value.unary(value.value.sin(), value.value.cos(), -value.value.sin())


def jet_cos(value):
    return value.unary(value.value.cos(), -value.value.sin(), -value.value.cos())


def jet_sqrt(value):
    root = value.value.sqrt()
    return value.unary(root, 1 / (2 * root), -1 / (4 * root**3))


def jet_dot(left, right):
    return left[0] * right[0] + left[1] * right[1]


def jet_atan2(y_value, x_value):
    radius_squared = x_value.value**2 + y_value.value**2
    radius_fourth = radius_squared**2
    partial_x = -y_value.value / radius_squared
    partial_y = x_value.value / radius_squared
    partial_xx = 2 * x_value.value * y_value.value / radius_fourth
    partial_xy = (y_value.value**2 - x_value.value**2) / radius_fourth
    partial_yy = -partial_xx
    gradient = [
        partial_x * x_value.gradient[i] + partial_y * y_value.gradient[i]
        for i in range(2)
    ]
    hessian = []
    for i in range(2):
        row = []
        for j in range(2):
            row.append(
                partial_x * x_value.hessian[i][j]
                + partial_y * y_value.hessian[i][j]
                + partial_xx * x_value.gradient[i] * x_value.gradient[j]
                + partial_xy
                * (
                    x_value.gradient[i] * y_value.gradient[j]
                    + y_value.gradient[i] * x_value.gradient[j]
                )
                + partial_yy * y_value.gradient[i] * y_value.gradient[j]
            )
        hessian.append(row)
    return Jet2(type(x_value.value).atan2(y_value.value, x_value.value), gradient, hessian)


def jet_collision(position, velocity, target):
    displacement = (
        position[0] - target.center[0],
        position[1] - target.center[1],
    )
    linear = jet_dot(displacement, velocity)
    offset = jet_dot(displacement, displacement) - target.radius**2
    discriminant = linear * linear - offset
    if not discriminant.value > 0:
        raise RuntimeError(f"jet discriminant is not positive: {discriminant.value}")
    flight = -linear - jet_sqrt(discriminant)
    if not flight.value > 0:
        raise RuntimeError(f"jet flight is not positive: {flight.value}")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    normal = (
        (impact[0] - target.center[0]) / target.radius,
        (impact[1] - target.center[1]) / target.radius,
    )
    normal_speed = jet_dot(velocity, normal)
    reflected = (
        velocity[0] - 2 * normal_speed * normal[0],
        velocity[1] - 2 * normal_speed * normal[1],
    )
    return impact, reflected


def return_map_jacobian(module, base_angle, slope, unstable, stable):
    """Return the complete connector map and its Jacobian in (a,b)."""

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
    first = module.FULL_OBSTACLES[0]
    position = (
        first.center[0] + first.radius * normal[0],
        first.center[1] + first.radius * normal[1],
    )
    for target in module.FULL_OBSTACLES[1:] + module.FULL_OBSTACLES[:1]:
        position, velocity = module.ray_circle_collision(position, velocity, target)

    final_normal = (
        (position[0] - first.center[0]) / first.radius,
        (position[1] - first.center[1]) / first.radius,
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
    image_unstable = (
        final_arclength + final_momentum.value / slope
    ) / 2
    image_stable = (
        final_arclength - final_momentum.value / slope
    ) / 2
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
    return image_unstable, image_stable, module.arb_mat([unstable_row, stable_row])


def centered_jacobian_enclosure(
    module, base_angle, slope, unstable_box, stable_box, unstable_center, stable_center
):
    """Enclose the Jacobian by a point value plus Hessian times tile radii."""

    unstable = Jet2(unstable_box, [module.arb(1), module.arb(0)])
    stable = Jet2(stable_box, [module.arb(0), module.arb(1)])
    arclength = unstable + stable
    momentum = slope * (unstable - stable)
    theta = Jet2(base_angle) + arclength / module.R_GRAY
    normal = jet_cos(theta), jet_sin(theta)
    tangent = -normal[1], normal[0]
    cosine_phi = jet_sqrt(1 - momentum * momentum)
    velocity = (
        cosine_phi * normal[0] + momentum * tangent[0],
        cosine_phi * normal[1] + momentum * tangent[1],
    )
    first = module.FULL_OBSTACLES[0]
    position = (
        first.center[0] + first.radius * normal[0],
        first.center[1] + first.radius * normal[1],
    )
    for target in module.FULL_OBSTACLES[1:] + module.FULL_OBSTACLES[:1]:
        position, velocity = jet_collision(position, velocity, target)
    final_normal = (
        (position[0] - first.center[0]) / first.radius,
        (position[1] - first.center[1]) / first.radius,
    )
    final_tangent = -final_normal[1], final_normal[0]
    final_angle = jet_atan2(final_normal[1], final_normal[0])
    final_momentum = jet_dot(velocity, final_tangent)
    final_arclength = module.R_GRAY * (final_angle - base_angle)
    outputs = (
        (final_arclength + final_momentum / slope) / 2,
        (final_arclength - final_momentum / slope) / 2,
    )

    _, _, center_matrix = return_map_jacobian(
        module, base_angle, slope, unstable_center, stable_center
    )
    unstable_radius = (unstable_box - unstable_center).abs_upper()
    stable_radius = (stable_box - stable_center).abs_upper()
    radii = (unstable_radius, stable_radius)
    rows = []
    for output_index, output in enumerate(outputs):
        row = []
        for derivative_index in range(2):
            error = sum(
                output.hessian[derivative_index][variable_index].abs_upper()
                * radii[variable_index]
                for variable_index in range(2)
            )
            row.append(center_matrix[output_index, derivative_index] + module.arb(0, error))
        rows.append(row)
    return module.arb_mat(rows), outputs, radii


def certify_unstable_cone(module, matrix, cone_width, expansion):
    """Check M{|db|<=k|da|} lies strictly inside the same cone."""

    ratio = module.arb(0, cone_width)
    dominant = matrix[0, 0] + matrix[0, 1] * ratio
    transverse = matrix[1, 0] + matrix[1, 1] * ratio
    if not dominant > expansion:
        raise RuntimeError(f"forward dominant expansion failed: {dominant}")
    margin = cone_width * dominant - transverse.abs_upper()
    if not margin > 0:
        raise RuntimeError(f"forward unstable cone failed: margin={margin}")
    return margin, dominant


def certify_inverse_stable_cone(module, matrix, cone_width, expansion):
    """Check the area-preserving inverse maps the stable cone strictly inside."""

    # Billiard collision maps preserve dr dp, and the same fixed linear
    # (a,b)->(r,p) chart is used at source and target.  Hence det M=1 exactly
    # and M^{-1} is its adjugate; this avoids interval determinant cancellation.
    inverse = module.arb_mat(
        [[matrix[1, 1], -matrix[0, 1]], [-matrix[1, 0], matrix[0, 0]]]
    )
    ratio = module.arb(0, cone_width)
    dominant = inverse[1, 0] * ratio + inverse[1, 1]
    transverse = inverse[0, 0] * ratio + inverse[0, 1]
    if not dominant > expansion:
        raise RuntimeError(f"inverse dominant expansion failed: {dominant}")
    margin = cone_width * dominant - transverse.abs_upper()
    if not margin > 0:
        raise RuntimeError(f"inverse stable cone failed: margin={margin}")
    return margin, dominant


def coefficient_enclosure(quartic, cubic, module, base_angle, slope, nodes):
    """Repeat the three-dimensional Krawczyk enclosure used by the parent."""

    quadratic, cubic_term = cubic.solve_point_system(
        module,
        base_angle,
        slope,
        nodes[0],
        nodes[2],
        module.arb("-0.000437419419665271895210239743171794"),
        module.arb(0),
    )
    centers = quartic.point_newton(
        module,
        base_angle,
        slope,
        nodes,
        [quadratic, cubic_term, module.arb("3e-42")],
    )
    radii = [module.arb("1e-60"), module.arb("1e-56"), module.arb("1e-52")]
    boxes = [centers[index] + module.arb(0, radii[index]) for index in range(3)]
    center_values = []
    interval_rows = []
    center_rows = []
    for stable in nodes:
        value, row = quartic.quartic_residual(
            module, base_angle, slope, centers, stable
        )
        _, interval_row = quartic.quartic_residual(
            module, base_angle, slope, boxes, stable
        )
        center_values.append([value])
        center_rows.append(row)
        interval_rows.append(interval_row)
    center_jacobian = module.arb_mat(center_rows)
    determinant = center_jacobian.det()
    if determinant.contains(0):
        raise RuntimeError(f"three-node center Jacobian is singular: {determinant}")
    inverse = center_jacobian.inv()
    preconditioner = module.arb_mat(3, 3)
    for row in range(3):
        for column in range(3):
            preconditioner[row, column] = module.arb(
                inverse[row, column].str(100, radius=False, more=True)
            )
    identity = module.arb_mat(3, 3)
    for index in range(3):
        identity[index, index] = module.arb(1)
    center_vector = module.arb_mat([[entry] for entry in centers])
    centered_box = module.arb_mat([[module.arb(0, radius)] for radius in radii])
    image = (
        center_vector
        - preconditioner * module.arb_mat(center_values)
        + (identity - preconditioner * module.arb_mat(interval_rows)) * centered_box
    )
    for index, box in enumerate(boxes):
        if not box.contains_interior(image[index, 0]):
            raise RuntimeError(
                f"three-node Krawczyk inclusion failed at {index}: {image[index, 0]}"
            )
    return [image[index, 0] for index in range(3)], determinant


def main(thickness_text="1e-25"):
    quartic = load_module("cm2_strip_quartic", QUARTIC_CERT)
    cubic = quartic.load_module("cm2_strip_cubic", quartic.CUBIC_CERT)
    tile = cubic.load_module("cm2_strip_tile", cubic.TILE_CERT)
    point = tile.load_module("cm2_strip_point", tile.POINT_CERT)
    shooting = point.load_module("cm2_strip_shooting", point.SHOOTING_CERT)
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
    coefficients, determinant = coefficient_enclosure(
        quartic, cubic, module, base_angle, slope, nodes
    )

    strip_radius = module.arb("1e-22")
    subdivisions = 16
    thickness = module.arb(thickness_text)
    strip_left = midpoint - strip_radius
    strip_right = midpoint + strip_radius
    step = 2 * strip_radius / subdivisions
    minimum_flight = None
    minimum_discriminant = None
    minimum_incidence = None
    minimum_clearance = None
    minimum_forward_cone_margin = None
    minimum_inverse_cone_margin = None
    minimum_forward_expansion = None
    minimum_inverse_expansion = None
    maximum_unstable_radius = None
    cone_width = module.arb("1e-6")
    expansion = module.arb(100)

    for index in range(subdivisions):
        stable_center = strip_left + (module.arb(index) + module.arb("0.5")) * step
        stable = stable_center + module.arb(0, (step / 2).upper())
        polynomial = sum(
            coefficients[power - 2] * stable**power for power in range(2, 5)
        )
        unstable = polynomial + module.arb(0, thickness)
        unstable_center = sum(
            coefficients[power - 2] * stable_center**power
            for power in range(2, 5)
        )
        physical = shooting.certify_physical_tube(
            module, base_angle, slope, unstable, stable
        )
        centered_matrix, _, radii = centered_jacobian_enclosure(
            module,
            base_angle,
            slope,
            unstable,
            stable,
            unstable_center,
            stable_center,
        )
        forward_margin, forward_expansion = certify_unstable_cone(
            module, centered_matrix, cone_width, expansion
        )
        inverse_margin, inverse_expansion = certify_inverse_stable_cone(
            module, centered_matrix, cone_width, expansion
        )
        values = physical[2:6]
        minimum_flight = values[0] if minimum_flight is None or values[0] < minimum_flight else minimum_flight
        minimum_discriminant = values[1] if minimum_discriminant is None or values[1] < minimum_discriminant else minimum_discriminant
        minimum_incidence = values[2] if minimum_incidence is None or values[2] < minimum_incidence else minimum_incidence
        minimum_clearance = values[3] if minimum_clearance is None or values[3] < minimum_clearance else minimum_clearance
        minimum_forward_cone_margin = forward_margin if minimum_forward_cone_margin is None or forward_margin < minimum_forward_cone_margin else minimum_forward_cone_margin
        minimum_inverse_cone_margin = inverse_margin if minimum_inverse_cone_margin is None or inverse_margin < minimum_inverse_cone_margin else minimum_inverse_cone_margin
        minimum_forward_expansion = forward_expansion if minimum_forward_expansion is None or forward_expansion < minimum_forward_expansion else minimum_forward_expansion
        minimum_inverse_expansion = inverse_expansion if minimum_inverse_expansion is None or inverse_expansion < minimum_inverse_expansion else minimum_inverse_expansion
        maximum_unstable_radius = radii[0] if maximum_unstable_radius is None or radii[0] > maximum_unstable_radius else maximum_unstable_radius

    print("CONNECTOR_QUARTIC_PHYSICAL_STRIP: CERTIFIED")
    print(f"  interpolation_nodes={nodes}")
    print(f"  certified_stable_interval=[{strip_left}, {strip_right}]")
    print(f"  subdivisions={subdivisions}")
    print(f"  unstable_half_thickness={thickness}")
    print(f"  coefficient_enclosures={coefficients}")
    print(f"  three_node_jacobian_determinant={determinant}")
    print("  physical_word=14 collisions / 8 fixed-section returns on every tile")
    print(f"  minimum_flight={minimum_flight}")
    print(f"  minimum_target_discriminant={minimum_discriminant}")
    print(f"  minimum_incidence_cosine={minimum_incidence}")
    print(f"  minimum_unintended_obstacle_clearance={minimum_clearance}")
    print("  transparent_wall_crossings=0")
    print("CONNECTOR_QUARTIC_STRIP_CONES: CERTIFIED")
    print(f"  cone_width={cone_width}")
    print(f"  expansion_threshold>{expansion}")
    print(f"  maximum_unstable_tile_radius={maximum_unstable_radius}")
    print(f"  minimum_forward_cone_margin={minimum_forward_cone_margin}")
    print(f"  minimum_inverse_cone_margin={minimum_inverse_cone_margin}")
    print(f"  minimum_forward_dominant_expansion={minimum_forward_expansion}")
    print(f"  minimum_inverse_dominant_expansion={minimum_inverse_expansion}")
    print("COMMON_MAGNET: NOT CERTIFIED")
    print("  remaining=invariant stable boundaries and full-cross inequalities")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} [half_thickness]")
    main(sys.argv[1] if len(sys.argv) == 2 else "1e-25")
