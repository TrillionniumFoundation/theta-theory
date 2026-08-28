#!/usr/bin/env python3
"""Correlation-preserving true-graph matching audit for CM2 Gate 1.

The two source curves in this file are the *certified invariant graphs*, not
their eigentangents.  Their values and first derivatives are kept as rigorous
nuisance enclosures.  Each collision leg is evaluated by a freshly recentered
one-parameter Taylor model: the shooting-parameter dependence is retained in
an affine polynomial, while the graph and quadratic Taylor remainders are
propagated separately.  A second, recentered variational enclosure supplies
the interval Jacobian used by Krawczyk.

This certificate is deliberately fail-closed.  A Krawczyk inclusion certifies
only a transverse common vertex of the two finite graph images.  Four-face
full crossing and transported twisting require additional rectangle and loop
certificates and are never inferred here.

Dependency: python-flint == 0.9.0.
"""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
QNL_CERT = HERE / "cm2_gate1_qnl_unstable_graph_cert.py"
CONNECTOR_CERT = HERE / "cm2_gate1_connector_stable_graph_cert.py"
TANGENT_CERT = HERE / "cm2_gate1_tangent_line_matching_cert.py"
PRECISION_BITS = 500
PRECONDITIONER_DIGITS = 110

# These centers are independently Newton-refined below.  They are only seeds.
T_SEED = "-1.396101069259116746830594312272814e-9"
U_SEED = "2.186137101021440040809485447235071e-12"

# Certified graph classes imported from the two predecessor certificates.
QNL_GRAPH_RADIUS = "2e-9"
QNL_GRAPH_QUADRATIC = "1"
QNL_GRAPH_LIPSCHITZ = "1e-4"
CONNECTOR_GRAPH_RADIUS = "3e-12"
CONNECTOR_GRAPH_QUADRATIC = "1e-2"
CONNECTOR_GRAPH_LIPSCHITZ = "1e-8"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def symmetric_ball(module, radius):
    """A deliberately inflated Arb ball containing ``[-radius,radius]``."""

    radius = abs(radius)
    text = (4 * radius).str(130, radius=False, more=True)
    ball = module.arb(0, text)
    if not ball.contains(radius) or not ball.contains(-radius):
        raise RuntimeError(f"failed to make symmetric ball for {radius}")
    return ball


def mat_vec(module, matrix, vector):
    return [
        sum((matrix[i][j] * vector[j] for j in range(2)), module.arb(0))
        for i in range(2)
    ]


@dataclass
class Replay:
    center: list[object]
    linear: list[object]
    remainder: list[object]
    derivative_center: list[object]
    derivative_remainder: list[object]
    minima: dict[str, object]
    maximum_state_radius: object

    def value_at_center(self, module):
        return [
            self.center[i] + symmetric_ball(module, self.remainder[i])
            for i in range(2)
        ]

    def derivative_box(self, module):
        return [
            self.derivative_center[i]
            + symmetric_ball(module, self.derivative_remainder[i])
            for i in range(2)
        ]


def update_minimum(current, value):
    return value if current is None else current.min(value)


def tm_collision_step(qnl, connector, module, source, target, angle_box, momentum_box):
    """The tangent-certificate collision map, differentiated to order two.

    Unlike the connector graph helper, the two matching words use relative
    lifts and therefore legitimately visit the canonical ``(-3/2,3/2)^2``
    box rather than only the connector orbit's open fundamental square.
    """

    Jet2 = qnl.Jet2
    theta = Jet2.variable(module, angle_box, 0)
    momentum = Jet2.variable(module, momentum_box, 1)
    normal = theta.cos(), theta.sin()
    tangent_vector = -normal[1], normal[0]
    cosine_phi = (1 - momentum * momentum).sqrt()
    velocity = (
        cosine_phi * normal[0] + momentum * tangent_vector[0],
        cosine_phi * normal[1] + momentum * tangent_vector[1],
    )
    position = (
        source.center[0] + source.radius * normal[0],
        source.center[1] + source.radius * normal[1],
    )
    displacement = (
        position[0] - target.center[0],
        position[1] - target.center[1],
    )
    linear = qnl.jet_dot(displacement, velocity)
    offset = qnl.jet_dot(displacement, displacement) - target.radius**2
    discriminant = linear * linear - offset
    if not discriminant.value > 0:
        raise RuntimeError(f"target discriminant may vanish: {discriminant.value}")
    flight = -linear - discriminant.sqrt()
    if not flight.value > 0:
        raise RuntimeError(f"target flight may be nonpositive: {flight.value}")
    impact = (
        position[0] + flight * velocity[0],
        position[1] + flight * velocity[1],
    )
    target_normal = (
        (impact[0] - target.center[0]) / target.radius,
        (impact[1] - target.center[1]) / target.radius,
    )
    incidence = -qnl.jet_dot(velocity, target_normal)
    if not incidence.value > 0:
        raise RuntimeError(f"target incidence may vanish: {incidence.value}")
    reflected = (
        velocity[0] + 2 * incidence * target_normal[0],
        velocity[1] + 2 * incidence * target_normal[1],
    )
    output_angle = qnl.jet_atan2(module, target_normal[1], target_normal[0])
    output_tangent = -target_normal[1], target_normal[0]
    output_momentum = qnl.jet_dot(reflected, output_tangent)
    canonical_bound = module.arb(3) / 2
    source_value = position[0].value, position[1].value
    target_value = impact[0].value, impact[1].value
    for endpoint in (source_value, target_value):
        if not (
            endpoint[0] > -canonical_bound
            and endpoint[0] < canonical_bound
            and endpoint[1] > -canonical_bound
            and endpoint[1] < canonical_bound
        ):
            raise RuntimeError(f"canonical endpoint leaves (-3/2,3/2)^2: {endpoint}")
    clearance = connector.segment_clearance(
        module, source_value, target_value, source, target
    )
    return connector.StepData(
        output_angle,
        output_momentum,
        source_value,
        target_value,
        flight.value,
        discriminant.value,
        incidence.value,
        clearance,
    )


def replay_leg(
    qnl,
    connector,
    tangent,
    module,
    *,
    kind: str,
    word,
    parameter_center,
    parameter_radius,
    base_angle,
    slope,
    graph_quadratic,
    graph_lipschitz,
    base_angle_radius=None,
    terminal_momentum_sign=1,
):
    """Recenter a scalar Taylor model after every declared collision.

    At the source, eigen coordinates are ``(z,h(z))``.  The affine part uses
    the eigentangent ``h=0``; the full certified bounds on ``h`` and ``h'``
    enter, respectively, the value and variational remainders.
    """

    radius = abs(parameter_radius)
    graph_bound = graph_quadratic * (abs(parameter_center) + radius) ** 2
    center = [base_angle + parameter_center / module.R_GRAY, slope * parameter_center]
    linear = [1 / module.R_GRAY, slope]
    remainder = [graph_bound / module.R_GRAY, abs(slope) * graph_bound]
    if base_angle_radius is not None:
        remainder[0] += abs(base_angle_radius)
    derivative_center = [1 / module.R_GRAY, slope]
    derivative_remainder = [
        graph_lipschitz / module.R_GRAY,
        abs(slope) * graph_lipschitz,
    ]
    minima = {"flight": None, "discriminant": None, "incidence": None, "clearance": None}
    maximum_state_radius = module.arb(0)
    current_kind = kind
    cumulative_i = 0
    cumulative_j = 0

    for target_key in word:
        total_radius = [
            abs(linear[i]) * radius + remainder[i] for i in range(2)
        ]
        maximum_state_radius = maximum_state_radius.max(total_radius[0]).max(total_radius[1])
        state_boxes = [
            center[i] + symmetric_ball(module, total_radius[i]) for i in range(2)
        ]
        source = module.obstacle(current_kind, 0, 0)
        target = module.obstacle(*target_key)
        box_step = tm_collision_step(
            qnl, connector, module, source, target, state_boxes[0], state_boxes[1]
        )
        center_step = tm_collision_step(
            qnl, connector, module, source, target, center[0], center[1]
        )
        global_impact_x = box_step.impact[0] + cumulative_i
        global_impact_y = box_step.impact[1] + cumulative_j
        if not (
            global_impact_x > 0
            and global_impact_x < 1
            and global_impact_y > 0
            and global_impact_y < 1
        ):
            raise RuntimeError(
                "Taylor tube may cross a transparent wall: "
                f"({global_impact_x},{global_impact_y})"
            )
        box_jacobian = [box_step.angle.gradient, box_step.momentum.gradient]
        center_jacobian = [center_step.angle.gradient, center_step.momentum.gradient]
        hessians = [box_step.angle.hessian, box_step.momentum.hessian]

        new_center = [center_step.angle.value, center_step.momentum.value]
        new_linear = mat_vec(module, center_jacobian, linear)
        new_remainder = []
        derivative_variation = [[module.arb(0) for _ in range(2)] for _ in range(2)]
        for output in range(2):
            propagated = sum(
                (abs(box_jacobian[output][j]) * remainder[j] for j in range(2)),
                module.arb(0),
            )
            quadratic = sum(
                (
                    abs(hessians[output][j][k])
                    * total_radius[j]
                    * total_radius[k]
                    for j in range(2)
                    for k in range(2)
                ),
                module.arb(0),
            ) / 2
            new_remainder.append(propagated + quadratic)
            for j in range(2):
                derivative_variation[output][j] = sum(
                    (
                        abs(hessians[output][j][k]) * total_radius[k]
                        for k in range(2)
                    ),
                    module.arb(0),
                )

        new_derivative_center = mat_vec(module, center_jacobian, derivative_center)
        new_derivative_remainder = []
        for output in range(2):
            inherited = sum(
                (
                    abs(box_jacobian[output][j]) * derivative_remainder[j]
                    for j in range(2)
                ),
                module.arb(0),
            )
            varying_matrix = sum(
                (
                    derivative_variation[output][j] * abs(derivative_center[j])
                    for j in range(2)
                ),
                module.arb(0),
            )
            new_derivative_remainder.append(inherited + varying_matrix)

        for name, value in (
            ("flight", box_step.flight),
            ("discriminant", box_step.discriminant),
            ("incidence", box_step.incidence),
            ("clearance", box_step.clearance),
        ):
            minima[name] = update_minimum(minima[name], value)

        center = new_center
        linear = new_linear
        remainder = new_remainder
        derivative_center = new_derivative_center
        derivative_remainder = new_derivative_remainder
        cumulative_i += target_key[1]
        cumulative_j += target_key[2]
        current_kind = target_key[0]

    if terminal_momentum_sign == -1:
        center[1] = -center[1]
        linear[1] = -linear[1]
        derivative_center[1] = -derivative_center[1]
    elif terminal_momentum_sign != 1:
        raise ValueError("terminal_momentum_sign must be +/-1")
    return Replay(
        center,
        linear,
        remainder,
        derivative_center,
        derivative_remainder,
        minima,
        maximum_state_radius,
    )


def build_replays(module, root, slope_a, slope_b, t_center, u_center, t_radius, u_radius):
    qnl = load(QNL_CERT, "cm2_gate1_true_graph_qnl")
    connector = load(CONNECTOR_CERT, "cm2_gate1_true_graph_connector")
    tangent = load(TANGENT_CERT, "cm2_gate1_true_graph_tangent")
    expected = (
        (qnl.RADIUS, QNL_GRAPH_RADIUS, "QNL graph radius"),
        (qnl.QUADRATIC_CONSTANT, QNL_GRAPH_QUADRATIC, "QNL quadratic bound"),
        (qnl.LIPSCHITZ_CONSTANT, QNL_GRAPH_LIPSCHITZ, "QNL Lipschitz bound"),
        (connector.TARGET_RADIUS, CONNECTOR_GRAPH_RADIUS, "connector graph radius"),
        (
            connector.QUADRATIC_CONSTANT,
            CONNECTOR_GRAPH_QUADRATIC,
            "connector quadratic bound",
        ),
        (
            connector.LIPSCHITZ_CONSTANT,
            CONNECTOR_GRAPH_LIPSCHITZ,
            "connector Lipschitz bound",
        ),
    )
    for actual, frozen, label in expected:
        if actual != frozen:
            raise RuntimeError(f"{label} changed: predecessor={actual}, expected={frozen}")
    qnl_replay = replay_leg(
        qnl,
        connector,
        tangent,
        module,
        kind="G",
        word=tangent.QNL_FORWARD_WORD,
        parameter_center=t_center,
        parameter_radius=t_radius,
        base_angle=module.arb.pi() / 4,
        slope=slope_a,
        graph_quadratic=module.arb(QNL_GRAPH_QUADRATIC),
        graph_lipschitz=module.arb(QNL_GRAPH_LIPSCHITZ),
    )
    connector_center = root.centers[0]
    connector_base_radius = abs(root.boxes[0] - connector_center)
    connector_replay = replay_leg(
        qnl,
        connector,
        tangent,
        module,
        kind="G",
        word=tangent.CONNECTOR_REVERSE_FORWARD_WORD,
        parameter_center=u_center,
        parameter_radius=u_radius,
        base_angle=connector_center,
        slope=slope_b,
        graph_quadratic=module.arb(CONNECTOR_GRAPH_QUADRATIC),
        graph_lipschitz=module.arb(CONNECTOR_GRAPH_LIPSCHITZ),
        base_angle_radius=connector_base_radius,
        terminal_momentum_sign=-1,
    )
    return qnl_replay, connector_replay


def residual_and_jacobian(module, root, slope_a, slope_b, t, u, rt, ru):
    left, right = build_replays(module, root, slope_a, slope_b, t, u, rt, ru)
    left_value = left.value_at_center(module)
    right_value = right.value_at_center(module)
    values = [left_value[i] - right_value[i] for i in range(2)]
    left_derivative = left.derivative_box(module)
    right_derivative = right.derivative_box(module)
    jacobian = [
        [left_derivative[0], -right_derivative[0]],
        [left_derivative[1], -right_derivative[1]],
    ]
    return values, jacobian, left, right


def midpoint_decimal(value, digits=130):
    return value.str(digits, radius=False, more=True)


def tangent_center(module, root, slope_a, slope_b):
    tangent = load(TANGENT_CERT, "cm2_gate1_true_graph_tangent_center")
    return tangent.refine_center(module, root, slope_a, slope_b)


def rational_preconditioner(module, jacobian):
    inverse = module.arb_mat(jacobian).inv()
    rows = []
    for i in range(2):
        row = []
        for j in range(2):
            value = Fraction(midpoint_decimal(inverse[i, j], PRECONDITIONER_DIGITS))
            row.append(module.arb(module.fmpq(value.numerator, value.denominator)))
        rows.append(row)
    return module.arb_mat(rows)


def certify():
    tangent = load(TANGENT_CERT, "cm2_gate1_true_graph_setup")
    module = tangent.load_frozen_certificate()
    module.ctx.prec = PRECISION_BITS
    root, slope_a, slope_b = tangent.setup_fixed_data(module)
    t_decimal, u_decimal = tangent_center(module, root, slope_a, slope_b)
    t_center = module.arb(t_decimal)
    u_center = module.arb(u_decimal)

    # The actual-graph ordinate shifts are many orders larger than the old
    # affine-root radii.  These radii are chosen only after the Taylor audit;
    # the inclusion below, not this comment, is the acceptance criterion.
    t_radius_text = "1e-17"
    u_radius_text = "1e-20"
    t_radius = module.arb(t_radius_text)
    u_radius = module.arb(u_radius_text)
    t_delta = symmetric_ball(module, t_radius)
    u_delta = symmetric_ball(module, u_radius)
    # ``symmetric_ball`` is outward-inflated.  The derivative audit is run on
    # an even wider explicit model radius, so its Jacobian enclosure covers
    # the exact X used in the Krawczyk operator (and not merely the nominal
    # decimal radius).
    t_model_radius = 8 * t_radius
    u_model_radius = 8 * u_radius
    if not abs(t_delta) < t_model_radius or not abs(u_delta) < u_model_radius:
        raise RuntimeError("declared Taylor model radii do not cover Krawczyk X")
    if not abs(t_center) + t_model_radius < module.arb(QNL_GRAPH_RADIUS):
        raise RuntimeError("QNL Krawczyk box leaves certified graph domain")
    if not abs(u_center) + u_model_radius < module.arb(CONNECTOR_GRAPH_RADIUS):
        raise RuntimeError("connector Krawczyk box leaves certified graph domain")

    center_values, center_jacobian, left_center, right_center = residual_and_jacobian(
        module, root, slope_a, slope_b, t_center, u_center, module.arb(0), module.arb(0)
    )
    _, box_jacobian, left, right = residual_and_jacobian(
        module,
        root,
        slope_a,
        slope_b,
        t_center,
        u_center,
        t_model_radius,
        u_model_radius,
    )
    preconditioner = rational_preconditioner(module, center_jacobian)
    identity = module.arb_mat([[1, 0], [0, 1]])
    center_vector = module.arb_mat([[t_center], [u_center]])
    residual_vector = module.arb_mat([[center_values[0]], [center_values[1]]])
    centered_box = module.arb_mat([[t_delta], [u_delta]])
    krawczyk = (
        center_vector
        - preconditioner * residual_vector
        + (identity - preconditioner * module.arb_mat(box_jacobian)) * centered_box
    )
    t_box = t_center + t_delta
    u_box = u_center + u_delta

    determinant = module.arb_mat(box_jacobian).det()
    print(f"  tangent_center_t={t_center}")
    print(f"  tangent_center_u={u_center}")
    print(f"  center_residual_true_graph_enclosure={center_values}")
    print(f"  center_jacobian_true_graph_enclosure={module.arb_mat(center_jacobian)}")
    print(f"  box_jacobian_true_graph_enclosure={module.arb_mat(box_jacobian)}")
    print(f"  matching_jacobian_determinant={determinant}")
    print(f"  krawczyk_image={krawczyk}")
    print(f"  qnl_krawczyk_delta={t_delta}")
    print(f"  connector_krawczyk_delta={u_delta}")
    print(f"  qnl_jacobian_model_radius={t_model_radius}")
    print(f"  connector_jacobian_model_radius={u_model_radius}")
    print(f"  qnl_center_remainder={left_center.remainder}")
    print(f"  connector_center_remainder={right_center.remainder}")
    print(f"  qnl_box_remainder={left.remainder}")
    print(f"  connector_box_remainder={right.remainder}")
    print(f"  qnl_derivative_remainder={left.derivative_remainder}")
    print(f"  connector_derivative_remainder={right.derivative_remainder}")
    print(f"  qnl_maximum_state_radius={left.maximum_state_radius}")
    print(f"  connector_maximum_state_radius={right.maximum_state_radius}")

    if determinant.contains(0):
        raise RuntimeError(f"true-graph matching Jacobian may vanish: {determinant}")
    if not t_box.contains_interior(krawczyk[0, 0]):
        raise RuntimeError(f"t Krawczyk inclusion fails: X={t_box}, K={krawczyk[0,0]}")
    if not u_box.contains_interior(krawczyk[1, 0]):
        raise RuntimeError(f"u Krawczyk inclusion fails: X={u_box}, K={krawczyk[1,0]}")

    thresholds = {
        "flight": module.arb(1) / 10,
        "discriminant": module.arb(1) / 1000,
        "incidence": module.arb(1) / 2,
        "clearance": module.arb(1) / 10,
    }
    minima = {}
    for name, threshold in thresholds.items():
        minima[name] = left.minima[name].min(right.minima[name])
        if not minima[name] > threshold:
            raise RuntimeError(f"physical first-hit margin {name} fails: {minima[name]}")

    print("TRUE_TWO_GRAPH_KRAWCZYK: CERTIFIED")
    print(f"  arb_precision_bits={module.ctx.prec}")
    print(f"  t_box={t_box}")
    print(f"  u_box={u_box}")
    print("  qnl_source=actual W^u_loc(QNL), not eigentangent")
    print("  connector_source=actual W^s_loc(connector), not eigentangent")
    print("  replay=per-collision recentered affine Taylor model plus rigorous remainder")
    print(f"  qnl_collision_count={len(tangent.QNL_FORWARD_WORD)}")
    print(f"  connector_collision_count={len(tangent.CONNECTOR_REVERSE_FORWARD_WORD)}")
    for name, value in minima.items():
        print(f"  minimum_{name}={value}")
    print("  finite_lattice_first_hit_exhaustion=[-3,3]^2")
    print("COMMON_VERTEX: CERTIFIED")
    print("FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED")
    print("  missing=four-face rectangle crossing inequalities around this vertex")
    print("TRANSPORTED_TWISTING: NOT CERTIFIED")
    print("  missing=closed common-vertex loop derivative and four wedge signs")
    return 0


def main():
    try:
        return certify()
    except Exception as exc:
        print(f"TRUE_TWO_GRAPH_KRAWCZYK: FAILED: {exc}")
        print("COMMON_VERTEX: NOT CERTIFIED")
        print("FULL_CROSS_COMMON_VERTEX: NOT CERTIFIED")
        print("TRANSPORTED_TWISTING: NOT CERTIFIED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
